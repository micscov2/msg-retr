import mongoengine as me
from mongoengine import Document

me.connect("test")

class ChannelInfo(Document):
	topic = me.StringField(required=True)
	members = me.ListField(me.StringField(required=True))

channel_info = ChannelInfo(topic="Current", members=["Parvez", "Mukund"])
channel_info.save()

# Sample output from above code
# > db.channel_info.find().pretty()
# {
#         "_id" : ObjectId("58fe40031d41c80c708d6995"),
#         "topic" : "Current",
#         "members" : [
#                 "Parvez",
#                 "Mukund"
#         ]
# }

