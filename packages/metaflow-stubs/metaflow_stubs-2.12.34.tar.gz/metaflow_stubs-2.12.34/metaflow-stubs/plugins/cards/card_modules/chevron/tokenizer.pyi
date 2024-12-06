######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.12.34                                                                                #
# Generated on 2024-12-04T14:12:34.710462                                                            #
######################################################################################################

from __future__ import annotations



class ChevronError(SyntaxError, metaclass=type):
    ...

def grab_literal(template, l_del):
    """
    Parse a literal from the template
    """
    ...

def l_sa_check(template, literal, is_standalone):
    """
    Do a preliminary check to see if a tag could be a standalone
    """
    ...

def r_sa_check(template, tag_type, is_standalone):
    """
    Do a final checkto see if a tag could be a standalone
    """
    ...

def parse_tag(template, l_del, r_del):
    """
    Parse a tag from a template
    """
    ...

def tokenize(template, def_ldel = '{{', def_rdel = '}}'):
    """
    Tokenize a mustache template
    
    Tokenizes a mustache template in a generator fashion,
    using file-like objects. It also accepts a string containing
    the template.
    
    
    Arguments:
    
    template -- a file-like object, or a string of a mustache template
    
    def_ldel -- The default left delimiter
                ("{{" by default, as in spec compliant mustache)
    
    def_rdel -- The default right delimiter
                ("}}" by default, as in spec compliant mustache)
    
    
    Returns:
    
    A generator of mustache tags in the form of a tuple
    
    -- (tag_type, tag_key)
    
    Where tag_type is one of:
     * literal
     * section
     * inverted section
     * end
     * partial
     * no escape
    
    And tag_key is either the key or in the case of a literal tag,
    the literal itself.
    """
    ...

