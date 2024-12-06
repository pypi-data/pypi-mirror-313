/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */

import {
  ChatModel,
  IChatHistory,
  IChatMessage,
  INewMessage
} from '@jupyter/chat';
import type { BaseChatModel } from '@langchain/core/language_models/chat_models';
import {
  AIMessage,
  HumanMessage,
  mergeMessageRuns
} from '@langchain/core/messages';
import { UUID } from '@lumino/coreutils';
import { getErrorMessage } from './llm-models';
import { IAIProvider } from './token';

export type ConnectionMessage = {
  type: 'connection';
  client_id: string;
};

export class ChatHandler extends ChatModel {
  constructor(options: ChatHandler.IOptions) {
    super(options);
    this._aiProvider = options.aiProvider;
    this._aiProvider.modelChange.connect(() => {
      this._errorMessage = this._aiProvider.chatError;
    });
  }

  get provider(): BaseChatModel | null {
    return this._aiProvider.chatModel;
  }

  async sendMessage(message: INewMessage): Promise<boolean> {
    message.id = UUID.uuid4();
    const msg: IChatMessage = {
      id: message.id,
      body: message.body,
      sender: { username: 'User' },
      time: Date.now(),
      type: 'msg'
    };
    this.messageAdded(msg);

    if (this._aiProvider.chatModel === null) {
      const errorMsg: IChatMessage = {
        id: UUID.uuid4(),
        body: `**${this._errorMessage ? this._errorMessage : this._defaultErrorMessage}**`,
        sender: { username: 'ERROR' },
        time: Date.now(),
        type: 'msg'
      };
      this.messageAdded(errorMsg);
      return false;
    }

    this._history.messages.push(msg);

    const messages = mergeMessageRuns(
      this._history.messages.map(msg => {
        if (msg.sender.username === 'User') {
          return new HumanMessage(msg.body);
        }
        return new AIMessage(msg.body);
      })
    );

    this.updateWriters([{ username: 'AI' }]);
    return this._aiProvider.chatModel
      .invoke(messages)
      .then(response => {
        const content = response.content;
        const botMsg: IChatMessage = {
          id: UUID.uuid4(),
          body: content.toString(),
          sender: { username: 'AI' },
          time: Date.now(),
          type: 'msg'
        };
        this.messageAdded(botMsg);
        this._history.messages.push(botMsg);
        return true;
      })
      .catch(reason => {
        const error = getErrorMessage(this._aiProvider.name, reason);
        const errorMsg: IChatMessage = {
          id: UUID.uuid4(),
          body: `**${error}**`,
          sender: { username: 'ERROR' },
          time: Date.now(),
          type: 'msg'
        };
        this.messageAdded(errorMsg);
        return false;
      })
      .finally(() => {
        this.updateWriters([]);
      });
  }

  async getHistory(): Promise<IChatHistory> {
    return this._history;
  }

  dispose(): void {
    super.dispose();
  }

  messageAdded(message: IChatMessage): void {
    super.messageAdded(message);
  }

  private _aiProvider: IAIProvider;
  private _errorMessage: string = '';
  private _history: IChatHistory = { messages: [] };
  private _defaultErrorMessage = 'AI provider not configured';
}

export namespace ChatHandler {
  export interface IOptions extends ChatModel.IOptions {
    aiProvider: IAIProvider;
  }
}
