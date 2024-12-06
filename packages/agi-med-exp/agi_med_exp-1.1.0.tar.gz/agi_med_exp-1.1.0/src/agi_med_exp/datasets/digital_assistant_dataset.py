import copy
import json
import codecs
import os
from typing import Any, Iterator

from agi_med_common.models import ChatItem


class DigitalAssistantDataset:
    """
    Represents a dataset for a digital assistant, loading and preparing data from chat and label files.
    """

    def __init__(self, chats_path: str, labels_path: str) -> None:
        """
        Initializes the DigitalAssistantDataset.

        Args:
            chats_path (str): Path to the directory containing chat JSON files.
            labels_path (str): Path to the directory containing label JSON files.
        """
        self.raw_chats, self.raw_labels = self.load_raw_data(chats_path, labels_path)
        self.cases, self.labels = self.prepare_data()
        self.index = 0

    @staticmethod
    def load_raw_data(chats_path: str, labels_path: str) -> tuple[list[dict], list[dict]]:
        """
        Loads raw chat and label data from the specified directories.

        Args:
            chats_path (str): Path to the directory containing chat JSON files.
            labels_path (str): Path to the directory containing label JSON files.

        Returns:
            Tuple[List[dict], List[dict]]: A tuple containing a list of chat dictionaries and a list of label
            dictionaries.

        Raises:
            FileNotFoundError: If no matching files are found between the chats and labels directories.
        """
        labels_files: set[str] = set(os.listdir(labels_path))
        chats_files: set[str] = set(os.listdir(chats_path))

        # Find matching chat and label files based on a portion of their filenames
        open_files = [file_name for file_name in labels_files if file_name[file_name.find("chatid") :] in chats_files]

        if not open_files:
            raise FileNotFoundError("No matching files found between chats and labels directories.")

        chats: list[dict] = []
        labels: list[dict] = []
        for file_name in open_files:
            chat_file_path: str = os.path.join(chats_path, file_name[file_name.find("chatid") :])
            label_file_path: str = os.path.join(labels_path, file_name)

            with codecs.open(chat_file_path, encoding="utf8") as f:
                chat: dict = json.load(f)
            with codecs.open(label_file_path, encoding="utf8") as f:
                label: dict = json.load(f)

            chats.append(chat)
            labels.append(label)

        return chats, labels

    @staticmethod
    def create_messages_label_from_chat_label(label: dict, messages: list[dict]) -> list[dict | None]:
        """
        Creates a list of message labels based on the provided chat label and messages.

        Args:
            label (dict): The chat label dictionary.
            messages (List[dict]): The list of message dictionaries.

        Returns:
            list: A list of message labels, where each element corresponds to a message in the input list.
                If a message has a 'Role' key, its label is set to None, otherwise it takes the chat label.
        """
        return [label if not m.get("Role") else None for m in messages]

    def prepare_data(self) -> tuple[list[tuple[str, ChatItem]], list[dict]]:
        """
        Prepares the loaded data into a format suitable for training or evaluation.

        Returns:
            Tuple[List[Tuple[str, ChatItem]], List[dict]]: A tuple containing:
                - A list of tuples, where each tuple consists of a replica (user utterance) and a ChatItem object
                representing the conversation context up to that point.
                - A list of labels corresponding to each replica in the first list.

        Raises:
            ValueError: If neither "messagesLabel" nor "chatLabel" is provided in a label dictionary.
            AssertionError: If the number of messages and labels do not match.
        """
        cases: list[tuple[str, ChatItem]] = []
        labels: list[dict] = []
        for chat, label in zip(self.raw_chats, self.raw_labels):
            messages: list[dict] = chat["InnerContext"]["Replicas"]

            # Determine message labels based on available label types
            if label.get("messagesLabel") is not None:
                m_labels: list[dict | None] = label["messagesLabel"]
            elif label.get("chatLabel") is not None:
                m_labels = self.create_messages_label_from_chat_label(label["chatLabel"], messages)
            else:
                raise ValueError('Either "messagesLabel" or "chatLabel" must be provided for each label.')

            assert len(messages) == len(m_labels), "Number of messages and labels do not match."

            for idx, (m, l) in enumerate(zip(messages, m_labels)):
                if l is not None:
                    replica: str = m["Body"]
                    case_chat: dict[str, Any] = copy.deepcopy(chat)
                    case_chat["InnerContext"]["Replicas"] = copy.deepcopy(messages[:idx])
                    case_chat["OuterContext"]["Age"] = int(case_chat["OuterContext"]["Age"])
                    case_chat_item = ChatItem.model_validate(case_chat)

                    cases.append((replica, case_chat_item))
                    labels.append(l)
        return cases, labels

    def make_table(self) -> dict[str, list]:
        cases, labels = self.prepare_data()
        return {
            "sex": [case[1].outer_context.sex for case in cases],
            "age": [case[1].outer_context.age for case in cases],
            "user": [case[1].outer_context.user_id for case in cases],
            "session": [case[1].outer_context.session_id for case in cases],
            "client": [case[1].outer_context.client_id for case in cases],
            "track": [case[1].outer_context.track_id for case in cases],
            "replica": [case[0] for case in cases],
            "label": labels,
        }

    def __len__(self) -> int:
        """
        Returns the total number of cases in the dataset.
        """
        return len(self.cases)

    def __getitem__(self, index: int) -> tuple[str, ChatItem, dict]:
        """
        Allows accessing a specific case in the dataset using its index.

        Args:
            index (int): The index of the desired case.

        Returns:
            Tuple[str, ChatItem, dict]: A tuple containing the replica, chat context, and label for the specified index.

        Raises:
            IndexError: If the provided index is out of range.
        """
        if index < 0 or index >= len(self):
            raise IndexError("Index out of range.")
        replica, chat = self.cases[index]
        label = self.labels[index]
        return replica, chat, label

    def __iter__(self) -> Iterator[tuple[str, ChatItem, dict]]:
        """
        Makes the dataset iterable, allowing you to iterate through its cases.
        """
        self.index = 0
        return self

    def __next__(self) -> tuple[str, ChatItem, dict]:
        """
        Returns the next case in the iteration.

        Raises:
            StopIteration: If there are no more cases to iterate over.
        """
        if self.index >= len(self):
            raise StopIteration
        result: tuple[str, ChatItem, dict] = self[self.index]
        self.index += 1
        return result
