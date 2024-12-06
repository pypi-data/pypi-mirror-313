from bs4 import BeautifulSoup as bs
from copy import deepcopy
from plone.restapi.blocks import iter_block_transform_handlers
from plone.restapi.blocks import visit_blocks
from plone.restapi.interfaces import IBlockFieldSerializationTransformer
from rer.newsletter.blocks_converter.slate2html import slate_to_html
from rer.newsletter.interfaces import IBlocksToHtml
from zope.interface import implementer


@implementer(IBlocksToHtml)
class BlocksToHtmlConverter:
    """
    Utility to convert blocks into html
    """

    def __call__(self, context, blocks, blocks_layout):
        blocks = self.get_blocks(
            context=context, blocks=blocks, blocks_layout=blocks_layout
        )
        if not blocks:
            return ""
        html = []
        for block in blocks:
            handler = getattr(
                self, f"block_handler_{block.get('@type', '')}", None
            )
            if handler and callable(handler):
                value = handler(context=context, block=block)
                if value:
                    html.append(value)
        root = "".join(html)
        soup = bs(root, "html.parser")  # make BeautifulSoup
        return soup.prettify()  # prettify the html

    def get_blocks(self, context, blocks, blocks_layout):
        """
        Return a list of ordered converted blocks
        """
        if not blocks:
            return []
        converted_blocks = deepcopy(blocks)
        # serialize blocks
        for block in visit_blocks(context, converted_blocks):
            new_block = block.copy()
            for handler in iter_block_transform_handlers(
                context, block, IBlockFieldSerializationTransformer
            ):
                new_block = handler(new_block)
            block.clear()
            block.update(new_block)
        ordered_blocks = []
        for block_id in blocks_layout.get("items", []):
            if block_id in converted_blocks:
                ordered_blocks.append(converted_blocks[block_id])
        return ordered_blocks

    def block_handler_slate(self, block, context=None):
        """
        Return converted slate block to HTML
        """
        return slate_to_html(block.get("value", []))

    def block_handler_image(self, block, context=None):
        """
        Return converted image block to HTML
        """
        scales_mapping = {"l": "large", "s": "mini", "m": "preview"}
        image_scales = block.get("image_scales", {}).get("image", [])
        if not image_scales:
            return ""

        image_scales = image_scales[0]
        align = block.get("align", "")
        root_classes = ["block", "image"]

        if align == "full":
            image_scale = image_scales
        else:
            image_scale = image_scales["scales"].get(
                scales_mapping.get(block.get("size", "")), {}
            )
            if not image_scale:
                image_scale = image_scales
            if align:
                root_classes.extend(["align", align])
        if not image_scale:
            return ""

        root = bs("<p></p>", "html.parser")
        root.p["class"] = root_classes
        img_tag = root.new_tag(
            "img",
            src=f"{block['url']}/{image_scale['download']}",
        )
        root.p.append(img_tag)
        return root.prettify()

    def block_handler_gridBlock(self, block, context):
        """
        Return converted grid block to HTML
        """
        blocks = self.get_blocks(
            context=context,
            blocks=block.get("blocks", {}),
            blocks_layout=block.get("blocks_layout", {}),
        )
        if not blocks:
            return ""
        root = bs(
            '<table class="gridBlock"><tbody><tr></tr></tbody></table>',
            "html.parser",
        )
        tr = root.findAll("tr")[0]

        for block in blocks:
            handler = getattr(
                self, f"block_handler_{block.get('@type', '')}", None
            )
            if handler and callable(handler):
                value = handler(block)
                if value:
                    el = bs(value, "html.parser")
                    td = root.new_tag("td", attrs={"class": "column"})
                    td.append(el)
                    tr.append(td)
        return root.prettify()  # prettify the html


blocks_to_html = BlocksToHtmlConverter()
