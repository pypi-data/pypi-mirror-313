use itertools::Itertools;
use syntax::SyntaxNode;
use text::Offset;

use crate::AstNode;

pub fn find_node_at_offset<N: AstNode>(syntax: &SyntaxNode, offset: Offset) -> Option<N> {
    ancestors_at_offset(syntax, offset).find_map(N::cast)
}

pub fn ancestors_at_offset(
    node: &SyntaxNode,
    offset: Offset,
) -> impl Iterator<Item = SyntaxNode> {
    node.token_at_offset(offset)
        .map(|token| token.parent_ancestors())
        .kmerge_by(|node1, node2| node1.text_span().len() < node2.text_span().len())
}
