# from aws_xray_sdk.core import patch_all
# from aws_xray_sdk.core import xray_recorder
# # noinspection PyUnresolvedReferences
# from aws_xray_sdk.ext.flask.middleware import XRayMiddleware
# from tabulate import tabulate
# from osbot_utils.utils.Json import json_save
# from osbot_utils.utils.Files import temp_file, file_exists, file_delete
# from cbr_website_beta.utils.Web_Utils import Web_Utils
#
# CBR_XRAY_SERVICE   = "CBR - XRay Service"
# XRAY_SEGMENT_NAME  = "CBR - XRay Segment"
#
# def xray_middleware(app):
#     if Web_Utils.running_in_aws():                          # only enable this when running in AWS
#         patch_all()                                         # patch the methods in from aws_xray_sdk.core.patcher import SUPPORTED_MODULES
#         xray_recorder.configure(service=CBR_XRAY_SERVICE)   # configure xray_recorder
#         XRayMiddleware(app, xray_recorder)                  # wired up XRayMiddleware
#
# def current_segment():
#     return xray_recorder.current_segment()
#
# def current_segment_name():
#     segment = current_segment()
#     if segment:
#         return segment.name
#     else:
#         return "...no segment..."
#
# def current_segment_data():
#     segment = current_segment()
#     if segment:
#         return segment.to_dict()
#     return {}
#
# def current_segment_print():
#     def extract_segment_data_for_hierarchical_markdown(segment, level=0, time_elapsed=0.0):
#         rows = []
#         name = segment.get('name', 'Unknown')
#
#         # Fetch additional annotations like AWS operation or bucket name
#         aws_info = segment.get('aws', {})
#         operation = aws_info.get('operation', '')
#         bucket_name = aws_info.get('bucket_name', '')
#
#         annotation = operation
#         if bucket_name:
#             annotation += f": {bucket_name}"
#
#         start_time = segment.get('start_time', 0.0)
#         end_time = segment.get('end_time', start_time)
#         duration = end_time - start_time
#         duration_s = f"{duration * 1000:.0f}ms" if duration < 1 else f"{duration:.2f}s"
#
#         indentation = '..' * level  # Two spaces per level for indentation
#
#         time_elapsed += duration
#         time_elapsed_s = f"{time_elapsed * 1000:.0f}ms" if time_elapsed < 1 else f"{time_elapsed:.2f}s"
#
#         # Fetch the HTTP response status, if available
#         http_info = segment.get('http', {})
#         response_info = http_info.get('response', {})
#         status = response_info.get('status', '-')
#
#         # Determine the segment status based on HTTP response or 'error' field
#         error = segment.get('error', False)
#         fault = segment.get('fault', False)
#         if error or fault:
#             segment_status = "Fault (5xx)"
#         else:
#             segment_status = "OK"
#
#         rows.append([f"..{indentation} {name}", annotation, segment_status, status, duration_s, time_elapsed_s])
#
#         for subsegment in segment.get('subsegments', []):
#             rows.extend(extract_segment_data_for_hierarchical_markdown(subsegment, level=level + 1, time_elapsed=time_elapsed))
#         return rows
#
#     segment_data = current_segment_data()
#
#     if segment_data:
#         # Extract data for hierarchical Markdown table
#         markdown_data_hierarchical = extract_segment_data_for_hierarchical_markdown(segment_data)
#
#         headers_md = ['Name', 'Annotation', 'Segment Status', 'Response Code', 'Duration', 'Time Elapsed']
#
#         # Generate the hierarchical Markdown table
#         markdown_table_hierarchical = tabulate(markdown_data_hierarchical, headers=headers_md, tablefmt='pipe')
#
#         print()
#         print(markdown_table_hierarchical)
#
#
# def current_segment_save_to(path=None):
#     segment = current_segment()
#     if segment:
#         if path is None:
#             path = temp_file(extension='.json')
#         file_delete(path)
#         assert file_exists(json_save(python_object=current_segment().to_dict(), path=path))
#         print(f"Segment saved to: {path}")
#         return path
#
# # def begin_segment():
# #     segment = xray_recorder.begin_segment(name=XRAY_SEGMENT_NAME)
# #     return segment
# #
# # def end_segment():
# #     xray_recorder.end_segment()