from os.path import exists
from pathlib import Path
from typing import Union, Optional, Dict, Any, List

import pandas as pd
from langchain_core.messages import HumanMessage, AIMessage

from ..agents import DataAnalystChatAgent
from .llm import AgentChatConsumer, current_app


class DataAnalystMixin:
    """데이터 분석 믹스인 클래스"""

    dataframe_path: Union[Path] = None
    column_guideline: str = ""

    def get_dataframe(self) -> pd.DataFrame:
        if getattr(self, "_dataframe", None) is None:
            dataframe_path = self.get_dataframe_path()
            if isinstance(dataframe_path, str):
                if not exists(dataframe_path):
                    dataframe_path = current_app(dataframe_path)
                dataframe_path = Path(dataframe_path)
            if not dataframe_path:
                raise ValueError("데이터프레임 파일 경로가 설정되지 않았습니다.")

            extension = dataframe_path.suffix.lower()
            if extension == ".csv":
                df = pd.read_csv(dataframe_path, encoding="utf-8")
            elif extension in (".xls", ".xlsx"):
                df = pd.read_excel(dataframe_path)
            else:
                raise ValueError(f"지원하지 않는 데이터프레임 파일 확장자: {extension}")

            setattr(self, "_dataframe", df)
        return getattr(self, "_dataframe")

    def get_dataframe_path(self) -> Optional[Union[str, Path]]:
        return self.dataframe_path

    def get_column_guideline(self) -> str:
        return self.column_guideline


class DataAnalystChatConsumer(DataAnalystMixin, AgentChatConsumer):
    """데이터 분석 채팅 컨슈머 클래스"""

    async def get_agent(
        self,
        initial_messages: Optional[List[Union[HumanMessage, AIMessage]]] = None,
    ) -> DataAnalystChatAgent:
        return DataAnalystChatAgent(
            llm=self.get_llm(),
            df=self.get_dataframe(),
            system_prompt=self.get_llm_system_prompt(),
            initial_messages=initial_messages,
            on_conversation_complete=self.on_conversation_complete,
            verbose=self.get_verbose(),
        )

    def get_llm_prompt_context_data(self) -> Dict[str, Any]:
        context_data = super().get_llm_prompt_context_data()
        context_data["dataframe_head"] = self.get_dataframe().head().to_markdown()
        context_data["column_guideline"] = self.get_column_guideline()
        return context_data
