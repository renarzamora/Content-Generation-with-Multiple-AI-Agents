from typing import Any, AsyncGenerator
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.conditions import MaxMessageTermination
from autogen_agentchat.ui import Console
from autogen_agentchat.base import TerminatedException, TerminationCondition, TaskResult
from autogen_agentchat.messages import StopMessage
from autogen_core import Component
from autogen_agentchat.messages import StructuredMessage
from schemas import ContentFeedback, SEOFeedback

load_dotenv()

class ScoreTerminationConfig(BaseModel):
    min_score_thresh: int

class ScoreTerminationCondition(TerminationCondition, Component[ScoreTerminationConfig]):
    component_config_schema = ScoreTerminationConfig # None

    def __init__(self, min_score_thresh: int = 8):
        self.min_score_thresh = min_score_thresh
        self._terminated = False
        self.min_content_score = 0
        self.seo_score = 0

    @property
    def terminated(self) -> bool:
        return self._terminated
     
    async def __call__(self, messages) -> StopMessage|None:
        if self._terminated:
            raise TerminatedException("Termination condition already met.")
            return None
        
        for message in messages:
            if message.source == "content_critic_agent":
                self.min_content_score = min(
                    message.content.grammar_score,
                    message.content.clarity_score,
                    message.content.style_score
                )
            elif message.source == "seo_critic_agent":
                self.seo_score = message.content.seo_score

        
        if self.min_content_score >= self.min_score_thresh and self.seo_score >= self.min_score_thresh:
            self._terminated = True
            return StopMessage(
                content=f"The minimun scrores are greater than or equal to {self.min_score_thresh}",
                source = "ScoreTermination",
            )
        return None

    async def reset(self) -> None:
        self._terminated = False

    def to_config(self) -> ScoreTerminationConfig:
        return ScoreTerminationConfig(min_score_thresh=self.min_score_thresh)

    @classmethod
    def _from_config(cls,config: ScoreTerminationConfig):
        return cls(min_score_thresh=config.min_score_thresh,)
    

async def teamconfig(min_score_thresh: int = 8) ->  SelectorGroupChat:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not found in your environment")
    
    model = OpenAIChatCompletionClient(
        model = 'o3-mini',
        api_key = api_key
    )

    writer_agent = AssistantAgent(
        name = "writer_agent",
        model_client = model,
        description = 'A writer agent that writes content based on a given topic.',
        system_message = "You are a writer agent You will be given a topic and you need to write some contetnt about it."
        'You will be collaborating with a content-critic agent and a SEO-critic agent. These agents '
        'will provide feedbacks and scores on your content. You should address their feedbacks and improve your content.'
        f'If both of the critic agents give you a minimum score of {min_score_thresh} in all of the scores, you should regenerate the content and '
        'then you should exactly say "TERMINATE"',
        )

    content_critic_agent = AssistantAgent(
        name = 'content_critic_agent',
        description = 'A content critic agent that provides feedbacks on the content written by the writer agent.',
        system_message = 'You are a content critic agent. You will be given a piece of text and you need to provide scores to 0 to 10 on '
        'the grammar, clarity and style of the text. You sshould also provide a to-do list of improvements for the writer agent.'
        'to improve the text.'
        'You should never write the text yourself. Be as specific as possible.'
        f'If the minimum score of the text is {min_score_thresh} or above {min_score_thresh}, leave the to-do list empty.',
        model_client = model,
        output_content_type = ContentFeedback

        )
    
    seo_critic_agent = AssistantAgent(
        name = 'seo_critic_agent',
        description = 'An SEO-critic agent that provides feedbacks on the SEO of the content written by the writer agent.',
        system_message = 'You are an SEO-critic agent. You will be given a piece of text and you need to provide a single score from 0 to 10 '
        "on the SEO of the text. You should also provide a to-do list of improvements for the writer agent."
        'You should never write the text yourself. Be as specific as possible.'
        f'If the minimum score of the text is {min_score_thresh} or above {min_score_thresh}, leave the to-do list empty.',
        model_client = model,
        output_content_type = SEOFeedback
        )

    selector_promt = """
    You are in a team of content generation agents. The following roles are available 
    {roles}.
    Read the following conversation. Then select the next role from {participants} to speak. Only return the roles.

    {history}
    If a critic agent has some to-do list for the writer agent,the writer agent should address it in the next message and that same critic agent should review the writer's agent message afterwards.
    Read the above conversation. Then select the next role from {participants} to speak. Only return the roles.    
    """

    termination = ScoreTerminationCondition(min_score_thresh) | MaxMessageTermination(15)

    team = SelectorGroupChat(
        participants = [writer_agent, content_critic_agent, seo_critic_agent],
        selector_prompt = selector_promt,
        termination_condition = termination,
        model_client = model,
        custom_message_types=[
        StructuredMessage[ContentFeedback],
        StructuredMessage[SEOFeedback],
        ],
        )

    return team



async def orchestrate(team, task):
    async for message in team.run_stream(task=task):
        if isinstance(message, TaskResult):
            yield msg
        else:
            print("==" * 20)
            if message.source == "writer_agent":
                print(msg:=f"**Writer**:\n\n{message.source}: {message.content} ")
                yield msg
            elif message.source == "content_critic_agent":
                print(msg:=f"**Content critic**:\n\n**{message.source}**: **Scores - Grammar**: {message.content.grammar_score},\n\n**Clarity**: {message.content.clarity_score},\n\n**Style**: {message.content.style_score},\n\n**To-Do**: {message.content.to_do_score}")
                yield msg
            elif message.source == "seo_critic_agent":
                
                print(msg:=f"**SEO Critic**:\n\n{message.source}: **SEO Score**: {message.content.seo_score},\n\nTo-Do: {message.content.to_do}")
                yield msg
            elif message.source == "user":
                print(msg:=f"**User**:\n\n{message.source}: {message.content}")
                yield msg