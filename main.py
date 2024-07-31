import argparse
import os
import multiprocessing
from abc import ABC, abstractmethod

class ParamProcessor(ABC):
    @abstractmethod
    def process(self, param: str, keyword: str) -> str:
        pass

class DefaultParamProcessor(ParamProcessor):
    def process(self, param: str, keyword: str) -> str:
        # Remove spaces from the param before concatenating
        param_no_spaces = param.replace(" ", "")
        return f"{param_no_spaces}{keyword}"

class FileHandler:
    @staticmethod
    def read_file(file_path: str) -> list:
        with open(file_path, 'r') as f:
            return [line.strip() for line in f if line.strip()]

    @staticmethod
    def write_file(file_path: str, content: str):
        with open(file_path, 'w') as f:
            f.write(content)

class ParamListProcessor:
    def __init__(self, processor: ParamProcessor):
        self.processor = processor

    def process_chunk(self, params: list, keyword: str) -> str:
        return ''.join([self.processor.process(param, keyword) for param in params])

def worker(chunk, keyword, processor, output_queue):
    result = processor.process_chunk(chunk, keyword)
    output_queue.put(result)

def split_list(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def main():
    parser = argparse.ArgumentParser(description="Process parameter lists")
    parser.add_argument("-u", "--input", required=True, help="Input text file")
    parser.add_argument("-p", "--keyword", required=True, help="Keyword to append")
    parser.add_argument("-s", "--split", type=int, required=True, help="Number of parameters per output file")
    parser.add_argument("-c", "--cores", type=int, default=2, help="Number of CPU cores to use")
    parser.add_argument("-e", "--remove_end", action="store_true", help="Remove the last character from each chunk")
    args = parser.parse_args()

    params = FileHandler.read_file(args.input)
    processor = ParamListProcessor(DefaultParamProcessor())

    chunk_size = max(1, len(params) // args.cores)
    chunks = list(split_list(params, chunk_size))

    output_queue = multiprocessing.Queue()
    processes = []

    for chunk in chunks:
        p = multiprocessing.Process(target=worker, args=(chunk, args.keyword, processor, output_queue))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    results = []
    while not output_queue.empty():
        results.append(output_queue.get())

    final_result = ''.join(results)

    base_name, ext = os.path.splitext(args.input)
    
    # Split the final result into chunks based on the number of parameters
    param_chunks = list(split_list(params, args.split))

    for i, param_chunk in enumerate(param_chunks):
        processed_chunk = ''.join([processor.processor.process(param, args.keyword) for param in param_chunk])
        if args.remove_end:
            processed_chunk = processed_chunk[:-1]  # Remove the last character
        output_file = f"{base_name}_{i:02}{ext}"
        FileHandler.write_file(output_file, processed_chunk)

if __name__ == "__main__":
    main()
