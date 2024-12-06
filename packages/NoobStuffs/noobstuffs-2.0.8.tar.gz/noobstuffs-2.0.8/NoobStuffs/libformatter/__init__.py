#
# Copyright (c) 2022 PrajjuS <theprajjus@gmail.com>.
#
# This file is part of NoobStuffs
# (see http://github.com/PrajjuS/NoobStuffs).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

"""Text Formatter Library"""

from typing import Optional

from .escape import TextEscape


class HTML:
    def bold(text: str):
        return f"<b>{TextEscape.html_escape(text)}</b>"

    def mono(text: str):
        return f"<code>{TextEscape.html_escape(text)}</code>"

    def pre(text: str):
        return f"<pre>{TextEscape.html_escape(text)}</pre>"

    def italic(text: str):
        return f"<i>{TextEscape.html_escape(text)}</i>"

    def underline(text: str):
        return f"<u>{TextEscape.html_escape(text)}</u>"

    def strike(text: str):
        return f"<s>{TextEscape.html_escape(text)}</s>"

    def spoiler(text: str):
        return f"<spoiler>{TextEscape.html_escape(text)}</spoiler>"

    def heading(text: str, size: int):
        if size == 1:
            return f"<h1>{TextEscape.html_escape(text)}</h1>"

        elif size == 2:
            return f"<h2>{TextEscape.html_escape(text)}</h2>"

        elif size == 3:
            return f"<h3>{TextEscape.html_escape(text)}</h3>"

        elif size == 4:
            return f"<h4>{TextEscape.html_escape(text)}</h4>"

        elif size == 5:
            return f"<h5>{TextEscape.html_escape(text)}</h5>"

        elif size == 6:
            return f"<h6>{TextEscape.html_escape(text)}</h6>"

        else:
            raise ValueError("Invalid size, use sizes between 1 to 6")

    def hyperlink(text: str, link: str):
        return f"<a href='{TextEscape.html_escape(link)}'>{TextEscape.html_escape(text)}</a>"

    def mention(text: str, uid: int):
        return f"<a href='tg://user?id={uid}'>{TextEscape.html_escape(text)}</a>"

    def invisible_link(link: str):
        return f"<a href='{TextEscape.html_escape(link)}'>\u2063</a>"

    def colon_item(key: str, value: str, mono_value: Optional[bool] = True):
        text = f"<b>{key}:</b> "
        text += f"<code>{value}</code>" if mono_value else f"{value}"
        return text


class MARKDOWN:
    def bold(text: str):
        return f"*{TextEscape.markdown_escape(text)}*"

    def mono(text: str):
        return f"`{TextEscape.markdown_escape(text)}`"

    def pre(text: str):
        return f"```{TextEscape.markdown_escape(text)}```"

    def italic(text: str):
        return f"_{TextEscape.markdown_escape(text)}_"

    def underline(text: str):
        return f"__{TextEscape.markdown_escape(text)}__"

    def strike(text: str):
        return f"~{TextEscape.html_escape(text)}~"

    def spoiler(text: str):
        return f"||{TextEscape.markdown_escape(text)}||"

    def heading(text: str, size: int):
        if size == 1:
            return f"#{TextEscape.html_escape(text)}#"

        elif size == 2:
            return f"##{TextEscape.html_escape(text)}##"

        elif size == 3:
            return f"###{TextEscape.html_escape(text)}###"

        elif size == 4:
            return f"####{TextEscape.html_escape(text)}####"

        elif size == 5:
            return f"#####{TextEscape.html_escape(text)}#####"

        elif size == 6:
            return f"######{TextEscape.html_escape(text)}######"

        else:
            raise ValueError("Invalid size, use sizes between 1 to 6")

    def hyperlink(text: str, link: str):
        return (
            f"[{TextEscape.markdown_escape(text)}]({TextEscape.markdown_escape(link)})"
        )

    def mention(text: str, uid: int):
        return f"[{TextEscape.markdown_escape(text)}](tg://user?id={uid})"

    def invisible_link(link: str):
        return f"[\u2063]({TextEscape.html_escape(link)})"

    def colon_item(key: str, value: str, mono_value: Optional[bool] = True):
        text = f"*{key}:* "
        text += f"`{value}`" if mono_value else f"{value}"
        return text
