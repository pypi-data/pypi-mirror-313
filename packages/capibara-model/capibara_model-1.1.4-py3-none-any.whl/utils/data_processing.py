"""
data_processing.py

This module provides functions for preprocessing training data for the CapibaraModel.
Includes functions for converting text to bytes and other data processing tasks.
"""

import logging
from typing import List, Tuple, Dict
import numpy as np #type: ignore

# Logger configuration
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def text_to_bytes(text: str) -> List[int]:
    """
    Converts given text to a list of bytes using UTF-8.

    Args:
        text (str): The input text to convert to bytes.

    Returns:
        List[int]: The list of bytes representing the input text.

    Raises:
        UnicodeEncodeError: If the text cannot be encoded using UTF-8.
    """
    try:
        return list(text.encode('utf-8'))
    except UnicodeEncodeError as e:
        logger.error(f"Error converting text to bytes: {str(e)}")
        raise


def bytes_to_text(bytes_list: List[int]) -> str:
    """
    Converts a list of bytes to text using UTF-8.

    Args:
        bytes_list (List[int]): The list of bytes to convert to text.

    Returns:
        str: The text representation of the input bytes.

    Raises:
        UnicodeDecodeError: If the bytes cannot be decoded using UTF-8.
    """
    try:
        return bytes(bytes_list).decode('utf-8', errors='replace')
    except UnicodeDecodeError as e:
        logger.error(f"Error converting bytes to text: {str(e)}")
        raise


def prepare_training_data(texts: List[str]) -> List[Tuple[List[int], List[int]]]:
    """
    Prepares training data by preprocessing texts and converting them to bytes.

    The target data is a circularly shifted version of the input data to simulate
    next-token prediction.

    Args:
        texts (List[str]): The list of input texts for training.

    Returns:
        List[Tuple[List[int], List[int]]]: The prepared training data as a list of tuples,
                                           where each tuple contains the input bytes and target bytes.
    """
    training_data = []
    for text in texts:
        input_bytes = text_to_bytes(text)
        target_bytes = input_bytes[1:] + [input_bytes[0]]
        training_data.append((input_bytes, target_bytes))
    return training_data


def load_training_data(file_path: str) -> List[str]:
    """
    Loads training data from a file.

    Args:
        file_path (str): The path to the file containing the training data.

    Returns:
        List[str]: The list of training texts loaded from the file.

    Raises:
        FileNotFoundError: If the specified file path does not exist.
        IOError: If there is an error reading the file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        logger.error(f"Training data file not found: {file_path}")
        raise
    except IOError as e:
        logger.error(f"Error loading training data from {file_path}: {str(e)}")
        raise


def save_preprocessed_data(preprocessed_data: List[Tuple[List[int], List[int]]], file_path: str) -> None:
    """
    Saves preprocessed training data to a file.

    Args:
        preprocessed_data (List[Tuple[List[int], List[int]]]): The preprocessed training data to save.
        file_path (str): The path to the file where the preprocessed data will be saved.

    Raises:
        IOError: If there is an error writing to the file.
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            for input_bytes, target_bytes in preprocessed_data:
                input_text = bytes_to_text(input_bytes)
                target_text = bytes_to_text(target_bytes)
                file.write(f"{input_text}\t{target_text}\n")
    except IOError as e:
        logger.error(f"Error saving preprocessed data to {file_path}: {str(e)}")
        raise


def postprocess_output(output_bytes: List[int]) -> str:
    """
    Converts output bytes to text.

    Args:
        output_bytes (List[int]): The output bytes to postprocess.

    Returns:
        str: The postprocessed output text.
    """
    return bytes_to_text(output_bytes)


def process_batch(batch: Dict) -> Dict:
    """Process a batch of data."""
    return {
        'inputs': np.array(batch['input_ids']),
        'context': np.array(batch['context_ids']),
        'targets': np.array(batch['target_ids']),
        'attention_mask': np.array(batch['attention_mask'])
    }
