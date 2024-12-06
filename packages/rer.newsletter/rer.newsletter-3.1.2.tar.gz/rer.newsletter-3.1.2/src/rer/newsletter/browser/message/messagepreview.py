# -*- coding: utf-8 -*-
from datetime import datetime
from Products.Five import BrowserView
from rer.newsletter.behaviors.ships import IShippable
from rer.newsletter.content.channel import Channel


DEFAULT_STYLES = """
.block.image {
  clear:both;
}
.block.align.right img {
    margin-left: 1em;
    margin-bottom: 1em;
    float: right;
}
.block.align.left img {
    margin-right: 1em;
    margin-bottom: 1em;
    float: left;
}
#footer {
    clear: both;
}
"""


class MessagePreview(BrowserView):
    """view for message preview"""

    def getMessageStyle(self):
        channel = None
        for obj in self.context.aq_chain:
            if isinstance(obj, Channel):
                channel = obj
                break
        if not channel:
            return DEFAULT_STYLES
        channel_styles = getattr(channel, "css_style", "") or ""
        return DEFAULT_STYLES + channel_styles

    @property
    def channel(self):
        for obj in self.context.aq_chain:
            if isinstance(obj, Channel):
                return obj
        return None

    def getMessageHeader(self):
        return getattr(self.channel, "header", "")

    def getMessageFooter(self):
        return getattr(self.channel, "footer", "")

    def getMessageSubHeader(self):
        return f"""
            <tr>
                <td align="left" colspan="2">
                  <div class="newsletterTitle">
                    <h1>{self.context.title}</h1>
                  </div>
                </td>
            </tr>
        """

    def getMessageContent(self):
        return f"""
            <tr>
                <td align="left" colspan="2">
                    {IShippable(self.context).message_content}
                </td>
            </tr>
        """

    def getMessagePreview(self):
        channel = None
        for obj in self.context.aq_chain:
            if isinstance(obj, Channel):
                channel = obj
                break
        if channel:
            body = ""
            body = channel.header if channel.header else ""
            body += f"""

                <tr>
                    <td align="left">
                        <div class="gmail-blend-screen">
                        <div class="gmail-blend-difference">
                            <div class="divider"></div>
                        </div>
                        </div>
                        <div class="newsletterTitle">
                        <h1>{self.context.title}</h1>
                        <h4 class="newsletterDate">{
                            datetime.today().strftime('Newsletter %d %B %Y')
                        }</h4>
                    </div>

                    </td>
                </tr>
                <tr>
                    <td align="left">
                     {IShippable(self.context).message_content}
                    </td>
                </tr>

            """
            body += channel.footer if channel.footer else ""

        return body
