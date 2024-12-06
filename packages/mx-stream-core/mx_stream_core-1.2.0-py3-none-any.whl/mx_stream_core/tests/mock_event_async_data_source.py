import os
import random
import socket
import threading
import time
from mx_stream_core.data_sources.base import BaseDataSource
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StructField, StringType, TimestampType

schema = StructType([
    StructField("timestamp", TimestampType()),
    StructField("topic", StringType()),
    StructField("data", StringType()),
    StructField("kafka_timestamp", TimestampType())
])


def socket_server(data, host, port, interval, mock_source):
    """
    Simulates a streaming socket server.
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Socket Server listening on {host}:{port}...")
    conn, addr = server_socket.accept()
    print(f"Connection from {addr}")
    try:
        for line in data:
            conn.sendall(f"{line}\n".encode("utf-8"))
            print(f"Sent: {line}")
            mock_source.event_count += 1
            time.sleep(interval)
    except BrokenPipeError:
        print("Client disconnected.")
    finally:
        conn.close()
        server_socket.close()
        mock_source.finished = True
        print("Socket server finished sending data.")


def file_stream_server(data, directory, interval, mock_source):
    """
    Simulates a streaming file source by writing data to a file incrementally.
    """
    # Cleanup existing files in the directory
    if os.path.exists(directory):
        for file in os.listdir(directory):
            file_path = os.path.join(directory, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        print(f"Cleared existing files in {directory}.")
    else:
        os.makedirs(directory)
        print(f"Created directory {directory}.")

    file_path = os.path.join(directory, "stream_data.txt")
    print(f"File stream server writing to {file_path}...")

    with open(file_path, "w") as file:
        for line in data:
            file.write(f"{line}\n")
            file.flush()  # Ensure the data is written immediately
            print(f"Written: {line}")
            mock_source.event_count += 1
            time.sleep(interval)

    mock_source.finished = True
    print("File stream server finished writing data.")


class MockAsyncDataSource(BaseDataSource):
    def __init__(self, spark: SparkSession, data, interval=5, mode="socket", file_stream_dir="tmp") -> None:
        """
        :param spark: SparkSession instance.
        :param data: List of data to simulate streaming.
        :param interval: Time interval between sending messages (default: 5 seconds).
        :param mode: Mode of streaming, either "socket" or "file" (default: "socket").
        :param file_stream_dir: Directory to store the file stream data (only used in file mode).
        """
        self.data = data
        self.spark = spark
        self.finished = False
        self.event_count = 0
        self.mode = mode
        self.file_stream_dir = file_stream_dir
        super().__init__()

        if mode == "socket":
            port = random.randint(9009, 25000)
            self.port = port
            server_thread = threading.Thread(
                target=socket_server,
                args=(data, "localhost", port, interval, self),
                daemon=True
            )
            server_thread.start()
        elif mode == "file":
            server_thread = threading.Thread(
                target=file_stream_server,
                args=(data, file_stream_dir, interval, self),
                daemon=True
            )
            server_thread.start()
        else:
            raise ValueError("Invalid mode. Choose either 'socket' or 'file'.")

    def get(self):
        """
        Returns a DataFrame for streaming based on the selected mode.
        """
        if self.mode == "socket":
            socket_df = self.spark.readStream.format("socket").option("host", "localhost").option("port",
                                                                                                  self.port).load()
            parsed_df = socket_df.withColumn("parsed_data", from_json(col("value"), schema)) \
                .select("parsed_data.*")
            return parsed_df
        elif self.mode == "file":
            file_df = self.spark.readStream.format("text").option("path", f"{self.file_stream_dir}").load()
            parsed_df = file_df.withColumn("parsed_data", from_json(col("value"), schema)) \
                .select("parsed_data.*")
            return parsed_df

    def awaitTermination(self):
        while not self.finished:
            time.sleep(1)
        print("Data source has finished processing all data.")
