# import speech_recognition as sr
# from queue import Queue
# import threading
#
#
# class BytePipe(Queue):
#     def get(self, block = True, timeout = None) -> bytes:
#         return super().get(block, timeout)
#
#     def put(self, item : bytes, block = True, timeout = None):
#         super().put(item, block, timeout)
#
#
# class Recorder:
#     def __init__(self):
#         self.recognizer = sr.Recognizer()
#         self.recognizer.non_speaking_duration = 0.1
#         self.recognizer.pause_threshold = 0.2
#         self.recognizer.energy_threshold = 750
#
#         self.is_running : bool = False
#         self.pipes: list[BytePipe] = []
#
#     def register_pipe(self) -> BytePipe:
#         pipe = BytePipe()
#         self.pipes.append(pipe)
#         return pipe
#
#     def start(self):
#         def do():
#             self.is_running = True
#             with sr.Microphone() as source:
#                 self.listen(source=source)
#         threading.Thread(target=do).start()
#
#     def stop(self):
#         self.is_running = False
#
#     def listen(self, source : sr.AudioSource):
#         while True:
#             if not self.is_running:
#                 break
#             audio_data = self.recognizer.listen(source)
#             wav_bytes = audio_data.get_wav_data()
#             for pipe in self.pipes:
#                 pipe.put(wav_bytes)
#
#
#
