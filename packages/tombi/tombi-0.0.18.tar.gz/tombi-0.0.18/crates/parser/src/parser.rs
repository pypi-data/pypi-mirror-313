use config::TomlVersion;
use syntax::{
    SyntaxKind::{self, *},
    T,
};

use crate::{input::Input, marker::Marker, token_set::TokenSet, Event};

#[derive(Debug)]
pub(crate) struct Parser<'t> {
    input: &'t Input,
    pos: usize,
    pub(crate) events: Vec<crate::Event>,
    toml_version: TomlVersion,
}

impl<'t> Parser<'t> {
    pub(crate) fn new(input: &'t Input, toml_version: TomlVersion) -> Self {
        Self {
            input,
            pos: 0,
            events: Vec::new(),
            toml_version,
        }
    }

    pub fn toml_version(&self) -> TomlVersion {
        self.toml_version
    }

    pub(crate) fn finish(self) -> Vec<crate::Event> {
        self.events
    }

    #[inline]
    pub(crate) fn current(&self) -> SyntaxKind {
        self.nth(0)
    }

    #[inline]
    pub(crate) fn current_range(&self) -> text::Range {
        self.input.range(self.pos)
    }

    #[inline]
    pub(crate) fn previous_range(&self) -> text::Range {
        match self.pos.checked_sub(1) {
            Some(pos) => self.input.range(pos),
            None => text::Range::default(),
        }
    }

    pub(crate) fn nth(&self, n: usize) -> SyntaxKind {
        self.input.kind(self.pos + n)
    }

    /// Checks if the current token is `kind`.
    pub(crate) fn at(&self, kind: SyntaxKind) -> bool {
        self.nth_at(0, kind)
    }

    pub(crate) fn nth_at(&self, n: usize, kind: SyntaxKind) -> bool {
        match kind {
            T!["[["] => self.at_composite2(n, T!['['], T!['[']),
            T!["]]"] => self.at_composite2(n, T![']'], T![']']),
            _ => self.input.kind(self.pos + n) == kind,
        }
    }

    pub(crate) fn nth_range(&self, n: usize) -> text::Range {
        self.input.range(self.pos + n)
    }

    fn at_composite2(&self, n: usize, k1: SyntaxKind, k2: SyntaxKind) -> bool {
        self.input.kind(self.pos + n) == k1
            && self.input.kind(self.pos + n + 1) == k2
            && self.input.is_joint(self.pos + n)
    }

    /// Consume the next token if `kind` matches.
    pub(crate) fn eat(&mut self, kind: SyntaxKind) -> bool {
        if !self.at(kind) {
            return false;
        }

        self.do_bump_kind(kind);

        true
    }

    pub(crate) fn eat_ts(&mut self, kinds: TokenSet) -> bool {
        let kind = self.current();
        if !kinds.contains(kind) {
            return false;
        }

        self.do_bump_kind(kind);

        true
    }

    /// Checks if the current token is in `kinds`.
    pub(crate) fn at_ts(&self, kinds: TokenSet) -> bool {
        kinds.contains(self.current())
    }

    /// Checks if the `n`-th token is in `kinds`.
    pub(crate) fn nth_at_ts(&self, n: usize, kinds: TokenSet) -> bool {
        kinds.contains(self.nth(n))
    }

    /// Starts a new node in the syntax tree. All nodes and tokens
    /// consumed between the `start` and the corresponding `Marker::complete`
    /// belong to the same node.
    pub(crate) fn start(&mut self) -> Marker {
        let event_index = self.events.len() as u32;
        self.push_event(Event::tombstone());
        Marker::new(event_index)
    }

    /// Consume the next token. Panics if the parser isn't currently at `kind`.
    pub(crate) fn bump(&mut self, kind: SyntaxKind) {
        assert!(self.eat(kind));
    }

    /// Advances the parser by one token
    pub(crate) fn bump_any(&mut self) {
        let kind = self.nth(0);
        if kind == EOF {
            return;
        }
        self.do_bump(kind, 1);
    }

    /// Advances the parser by one token, remapping its kind.
    /// This is useful to create contextual keywords from
    /// identifiers. For example, the lexer creates a `union`
    /// *identifier* token, but the parser remaps it to the
    /// `union` keyword, and keyword is what ends up in the
    /// final tree.
    pub(crate) fn bump_remap(&mut self, kind: SyntaxKind) {
        if self.nth(0) == EOF {
            // FIXME: panic!?
            return;
        }
        self.do_bump(kind, 1);
    }

    fn do_bump(&mut self, kind: SyntaxKind, n_raw_tokens: u8) {
        self.pos += n_raw_tokens as usize;
        self.push_event(Event::Token { kind, n_raw_tokens });
    }

    fn do_bump_kind(&mut self, kind: SyntaxKind) {
        let n_raw_tokens = match kind {
            T!["[["] | T!["]]"] => 2,
            _ => 1,
        };

        self.do_bump(kind, n_raw_tokens);
    }

    pub(crate) fn push_event(&mut self, event: Event) {
        self.events.push(event);
    }

    /// Emit error with the `message`
    /// FIXME: this should be much more fancy and support
    /// structured errors with spans and notes, like rustc
    /// does.
    pub(crate) fn error(&mut self, error: crate::Error) {
        self.push_event(Event::Error { error });
    }
}
