# import json


# class Element:

#     def __new__(cls, title: str, description: str, photo_id: =None, link: Optional[str]=None, buttons: Optional[list]=None, template_type: str="open_link"):
#         if template_type == "open_link":
#             return {
#                 "title": title,
#                 "description": description,
#                 "action": {
#                     "type": "open_link",
#                     "link": link
#                 },
#                 "photo_id": photo_id,
#                 "buttons": buttons
#             }
#         elif template_type == "open_photo":
#             return {
#                 "title": title,
#                 "description": description,
#                 "photo_id": photo_id,
#                 "action": {
#                     "type": "open_photo"
#                 },
#                 "buttons": buttons
#             }

# class Carousel:

#     def __init__(self, elements: list):
#         self.elements = elements

#     def add_carousel(self):
#         obj = json.dumps(
#             {
#                 "type": "carousel",
#                 "elements": self.elements
#             },
#             ensure_ascii=False
#         ).encode("utf-8")

#         return obj.decode("utf-8")

