class Prompt:
    def __init__(self, prompt_text: str, is_searchable: bool, searchable_text: str, is_user_prompt: bool, in_scope: bool, contains_context: bool):
        self._prompt_text = prompt_text
        self._is_searchable = is_searchable
        self._searchable_text = searchable_text
        self._is_user_prompt = is_user_prompt
        self._in_scope = in_scope
        self._contains_context = contains_context

    # Getter and Setter for prompt_text
    @property
    def prompt_text(self):
        return self._prompt_text

    @prompt_text.setter
    def prompt_text(self, value: str):
        self._prompt_text = value

    # Getter and Setter for is_searchable
    @property
    def is_searchable(self):
        return self._is_searchable

    @is_searchable.setter
    def is_searchable(self, value: bool):
        self._is_searchable = value

    # Getter and Setter for searchable_text
    @property
    def searchable_text(self):
        return self._searchable_text

    @searchable_text.setter
    def searchable_text(self, value: str):
        if self.is_searchable:  # Allow change only if is_searchable is True
            self._searchable_text = value
        else:
            raise ValueError("Cannot set searchable_text when is_searchable is False")

    # Getter and Setter for is_user_prompt
    @property
    def is_user_prompt(self):
        return self._is_user_prompt

    @is_user_prompt.setter
    def is_user_prompt(self, value: bool):
        self._is_user_prompt = value

    # Getter and Setter for in_scope
    @property
    def in_scope(self):
        return self._in_scope

    @in_scope.setter
    def in_scope(self, value: bool):
        self._in_scope = value

    @property
    def contains_context(self):
        return self._contains_context
    
    @contains_context.setter
    def contains_context(self, value: bool):
        self.contains_context = value
    
    def __str__(self):
        return f"Prompt(prompt_text='{self._prompt_text}', is_searchable={self._is_searchable}, " \
               f"searchable_text='{self._searchable_text}', is_user_prompt={self._is_user_prompt}, in_scope={self._in_scope})"
