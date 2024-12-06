use syntax::SyntaxKind;

use crate::{lexed, LexedStr};

pub struct Builder<'a, 'b> {
    pub(crate) lexed: &'a LexedStr<'a>,
    pub(crate) token_index: usize,
    pub(crate) state: State,
    pub(crate) sink: &'b mut dyn FnMut(lexed::Step<'_>),
}

impl std::fmt::Debug for Builder<'_, '_> {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("Builder")
            .field("lexed", &self.lexed)
            .field("token_index", &self.token_index)
            .field("state", &self.state)
            .finish()
    }
}

#[derive(Debug)]
pub enum State {
    PendingEnter,
    Normal,
    PendingExit,
}

impl<'a, 'b> Builder<'a, 'b> {
    pub fn new(lexed: &'a LexedStr<'a>, sink: &'b mut dyn FnMut(lexed::Step<'_>)) -> Self {
        Self {
            lexed,
            token_index: 0,
            state: State::PendingEnter,
            sink,
        }
    }

    pub fn token(&mut self, kind: SyntaxKind, n_tokens: u8) {
        match std::mem::replace(&mut self.state, State::Normal) {
            State::PendingEnter => unreachable!(),
            State::PendingExit => (self.sink)(lexed::Step::FinishNode),
            State::Normal => (),
        }
        self.eat_trivias();
        self.do_token(kind, n_tokens as usize);
    }

    pub fn enter(&mut self, kind: SyntaxKind) {
        match std::mem::replace(&mut self.state, State::Normal) {
            State::PendingEnter => {
                (self.sink)(lexed::Step::StartNode { kind });
                // No need to attach trivias to previous node: there is no
                // previous node.
                return;
            }
            State::PendingExit => (self.sink)(lexed::Step::FinishNode),
            State::Normal => (),
        }

        self.eat_n_trivias();
        (self.sink)(lexed::Step::StartNode { kind });
    }

    pub fn exit(&mut self) {
        match std::mem::replace(&mut self.state, State::PendingExit) {
            State::PendingEnter => unreachable!(),
            State::PendingExit => (self.sink)(lexed::Step::FinishNode),
            State::Normal => (),
        }
    }

    pub fn eat_trivias(&mut self) {
        while self.token_index < self.lexed.len() {
            let kind = self.lexed.kind(self.token_index);
            if !kind.is_trivia() {
                break;
            }
            self.do_token(kind, 1);
        }
    }

    fn n_trivias(&self) -> usize {
        (self.token_index..self.lexed.len())
            .take_while(|&it| self.lexed.kind(it).is_trivia())
            .count()
    }

    pub fn eat_n_trivias(&mut self) {
        for _ in 0..self.n_trivias() {
            let kind = self.lexed.kind(self.token_index);
            assert!(kind.is_trivia());
            self.do_token(kind, 1);
        }
    }

    pub fn do_token(&mut self, kind: SyntaxKind, n_tokens: usize) {
        let text = &self
            .lexed
            .range_text(self.token_index..self.token_index + n_tokens);
        self.token_index += n_tokens;

        (self.sink)(lexed::Step::AddToken { kind, text });
    }
}
