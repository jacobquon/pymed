from typing import TypeVar


def batches(iterable: list, n: int = 1) -> list:
    """ Helper method that creates batches from an iterable.

        Parameters:
            - iterable      Iterable, the iterable to batch.
            - n             Int, the batch size.

        Returns:
            - batches       List, yields batches of n objects taken from the iterable.
    """

    # Get the length of the iterable
    length = len(iterable)

    # Start a loop over the iterable
    for index in range(0, length, n):

        # Create a new iterable by slicing the original
        yield iterable[index : min(index + n, length)]


def getContent(
    element: TypeVar("Element"), path: str, default: str = None, separator: str = "\n"
) -> str:
    """ Internal helper method that retrieves the text content of an
        XML element.

        Parameters:
            - element   Element, the XML element to parse.
            - path      Str, Nested path in the XML element.
            - default   Str, default value to return when no text is found.

        Returns:
            - text      Str, text in the XML node.
    """

    # Find the path in the element
    result = element.findall(path)

    # Return the default if there is no such element
    if result is None or len(result) == 0:
        return default

    # Extract the text and return it
    else:
        return separator.join([sub.text for sub in result if sub.text is not None])

def getAbstract(
    element: TypeVar("Element"), path: str, default: str = None
) -> str:
    """ Internal helper method that retrieves the text content of an
        XML element.

        Parameters:
            - element   Element, the XML element to parse.
            - path      Str, Nested path in the XML element.
            - default   Str, default value to return when no text is found.

        Returns:
            - text      Str, text in the XML node.
    """

    ret_str = ""
    for top_level in element.findall(path): # Looping over bodies
        if top_level.find('sec') != None:
            for sec in top_level.findall('.//sec'): # Loop over all sections
                if sec.find('title') != None:
                    ret_str += " ".join(subtext.strip() for subtext in sec.find('title').itertext()) + ": " # Add the title (need to be careful of text being split by references or italics)
                if sec.find('p') != None:
                    for paragraph in sec.findall('p'):
                        ret_str += " ".join(subtext.strip() for subtext in paragraph.itertext()) + "\n" # Add the paragraph (need to be careful of text being split by references or italics)
        else:
            for sub in top_level:
                ret_str +=  " ".join(sub_2.strip() for sub_2 in sub.itertext()) + "\n"

    if len(ret_str) == 0:
        return default
    else:
        return ret_str

def getBody(
    element: TypeVar("Element"), path: str, default: str = None
) -> str:
    """ Internal helper method that retrieves the text content of an
        XML element.

        Parameters:
            - element   Element, the XML element to parse.
            - path      Str, Nested path in the XML element.
            - default   Str, default value to return when no text is found.

        Returns:
            - text      Str, text in the XML node.
    """

    ret_str = ""
    for top_level in element.findall(path): # Looping over bodies
        if top_level.find('sec') != None:
            for sec in top_level.findall('.//sec'): # Loop over all sections
                if sec.find('title') != None:
                    ret_str += " ".join(subtext.strip() for subtext in sec.find('title').itertext()) + ": " # Add the title (need to be careful of text being split by references or italics)
                if sec.find('p') != None:
                    for paragraph in sec.findall('p'):
                        ret_str += " ".join(subtext.strip() for subtext in paragraph.itertext()) + "\n\n" # Add the paragraph (need to be careful of text being split by references or italics)
        else:
            for sub in top_level:
                ret_str +=  " ".join(sub_2.strip() for sub_2 in sub.itertext()) + "\n\n"

    if len(ret_str) == 0:
        return default
    else:
        return ret_str

def getBodySections(
    element: TypeVar("Element"), path: str, default: str = None
) -> str:
    """ Internal helper method that retrieves the text content of an
        XML element.

        Parameters:
            - element   Element, the XML element to parse.
            - path      Str, Nested path in the XML element.
            - default   Str, default value to return when no text is found.

        Returns:
            - text      Str, text in the XML node.
    """

    # Get Introduction
    introductionStr = getSection(element, path, "introduction", default)
    # Get Methods
    methodsStr = getSection(element, path, "methods", default)
    # Get Results
    resultsStr = getSection(element, path, "results", default)
    # Get Discussion
    discussionStr = getSection(element, path, "discussion", default)
    # Get Conclusion
    conclusionStr = getSection(element, path, "conclusion", default)

    return introductionStr, methodsStr, resultsStr, discussionStr, conclusionStr


def getSection(
    element: TypeVar("Element"), path: str, section: str, default: str = None
) -> str:
    ret_str = ""
    for sec in element.findall(path): # Looping over sections within body
        if sec.find("title") != None and section in sec.findtext('title').lower(): # If the section is named as we're looking for it
            ret_str += " ".join(subtext.strip() for subtext in sec.find('title').itertext()) + ": "
            if sec.find('.//p') != None:
                for paragraph in sec.findall('.//p'):
                    ret_str += " ".join(subtext.strip() for subtext in paragraph.itertext()) + "\n\n" # Add the paragraph (need to be careful of text being split by references or italics)
    if len(ret_str) == 0:
        return default
    else:
        return ret_str
