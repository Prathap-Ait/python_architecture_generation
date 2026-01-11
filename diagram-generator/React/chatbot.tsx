import {
  DeleteOutlined,
  DownOutlined,
  MenuOutlined,
  MessageOutlined,
  PaperClipOutlined,
  PlusOutlined,
  SendOutlined,
  UpOutlined
} from '@ant-design/icons';
import { Button, Input, message as antdMessage, Tooltip } from 'antd';
import React, { useEffect, useRef, useState } from 'react';
import useJiraContext from 'src/hooks/useJiraContext';
import { BaseEditPageService } from 'src/services/baseEditPageService.sevice';
import { chatbotService } from 'src/services/chatbot.service';

import styles from './chatbot.module.scss';
// Helper class to fetch dynamic token
class AuthHelperService extends BaseEditPageService<any> {
  constructor() {
    super('chat-auth-init');
  }
}

interface MessageItem {
  role: 'user' | 'assistant';
  text: string;
  fileName?: string;
  fileType?: string;
  // timestamp optional
  ts?: number;
}

interface Chat {
  id: number;
  name: string;
  messages: MessageItem[];
  //session_id: string;
  // optional user identifiers cached per chat (for UI / debugging)
  user_account_id?: string;
  user_cloud_id?: string;
}

const STORAGE_KEY = 'fusefy_chatbot_chats_v2';

const Chatbot: React.FC = () => {
  // Get Jira context to retrieve siteUrl
  const { context } = useJiraContext();
  // const siteUrl = context?.siteUrl;
  const { siteUrl, environmentId, localId } = context;
  const appId = localId?.split('/')?.[1];

  // load initial state from localStorage or fallback
  const makeNewChat = (name = 'New Conversation'): Chat => ({
    id: Date.now() + Math.floor(Math.random() * 1000),
    name,
    messages: []
    //session_id: chatbotService.generate_random_session_id()
  });

  const [allChats, setAllChats] = useState<Chat[]>(() => {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (raw) {
        const parsed = JSON.parse(raw) as Chat[];
        // ensure session_id exists
        return parsed.map((c) => ({
          ...c
          //session_id: c.session_id || chatbotService.generate_random_session_id()
        }));
      }
    } catch (e) {
      // ignore parse errors
    }

    // default initial chats including document-upload mock flow
    return [
      makeNewChat(),

      // 1) Default welcome chat (kept same)
      {
        id: 1,
        name: 'Getting Started with Agentic AI',
        //session_id: chatbotService.generate_random_session_id(),
        messages: [
          {
            role: 'assistant',
            text: 'Welcome back to Fusefy AI! I’m your Agentic AI guide — here to help you explore how AI can think, act, and assist like a teammate.',
            ts: Date.now()
          },
          { role: 'user', text: 'That sounds interesting. What does “Agentic AI” mean?', ts: Date.now() },
          {
            role: 'assistant',
            text: 'Good question! Agentic AI goes beyond giving answers — it can take actions, like creating tasks, analyzing data, or triggering workflows securely.',
            ts: Date.now()
          }
        ]
      },

      // 2) NEW — Mock Conversation: Document Upload → Usecase Generation
      {
        id: 2,
        name: 'Usecase Generation Flow',
        //session_id: chatbotService.generate_random_session_id(),
        messages: [
          {
            role: 'assistant',
            text: 'Welcome to Fusefy AI.\n' + 'I am your Agentic AI guide. How can I assist you today?',
            ts: Date.now()
          },

          {
            role: 'user',
            text: 'I need to create a usecase.',
            ts: Date.now()
          },

          {
            role: 'assistant',
            text:
              'What kind of artifacts/documents will you provide?\n' +
              'These artifacts/documents are required to generate the usecase.\n\n' +
              'How many artifacts/documents will you be uploading?',
            ts: Date.now()
          },

          {
            role: 'user',
            text: '3 artifacts/documents.',
            ts: Date.now()
          },

          {
            role: 'assistant',
            text:
              'Understood.\n' +
              'Please provide the artifacts/documents.\n' +
              'Typical examples include API schemas, DB schemas, or instruction documents.',
            ts: Date.now()
          },

          // --- Artifact 1 ---
          {
            role: 'assistant',
            text: 'Please upload the API schema.',
            ts: Date.now()
          },
          {
            role: 'user',
            text: '',
            fileName: '📎 swagger_document.json',
            fileType: 'application/json',
            ts: Date.now()
          },
          {
            role: 'assistant',
            text: 'I have received your swagger_document.json.\n' + 'Please upload your DB schema.',
            ts: Date.now()
          },

          // --- Artifact 2 ---
          {
            role: 'user',
            text: '',
            fileName: '📎 db_schema.pdf',
            fileType: 'application/pdf',
            ts: Date.now()
          },
          {
            role: 'assistant',
            text: 'I have received your db_schema.pdf.\n' + 'Please upload your instructions document.',
            ts: Date.now()
          },

          // --- Artifact 3 ---
          {
            role: 'user',
            text: '',
            fileName: '📎 manual_instructions.pdf',
            fileType: 'application/pdf',
            ts: Date.now()
          },
          {
            role: 'assistant',
            text: 'I have received your manual_instructions.pdf.\n',
            ts: Date.now()
          },

          // --- Confirmation ---
          {
            role: 'assistant',
            text:
              'To confirm, you have uploaded:\n' +
              '1. swagger_document.json\n' +
              '2. db_schema.pdf\n' +
              '3. manual_instructions.pdf\n\n' +
              'Based on these, do you want me to create the usecase, or do you have more artifacts to upload?',
            ts: Date.now()
          },

          {
            role: 'user',
            text: 'Proceed with creating usecase. Good to go.',
            ts: Date.now()
          },

          // --- UPDATED TEXT HERE ---
          {
            role: 'assistant',
            text: 'Usecase creation is in progress. Stay tuned.',
            ts: Date.now()
          },
          {
            role: 'assistant',
            text: 'Your usecase has been created.\n' + 'Click AI INVENTORY to see the created usecase.',
            ts: Date.now()
          },
          {
            role: 'assistant',
            text: 'If there are no changes, would you like to create an AI Process?',
            ts: Date.now()
          },
          {
            role: 'user',
            text: 'Yes, proceed.',
            ts: Date.now()
          },
          {
            role: 'assistant',
            text: 'Processing AI Process...',
            ts: Date.now()
          },
          {
            role: 'assistant',
            text: 'Your AI Lifecycle has been created.',
            ts: Date.now()
          },

          // Architecture
          {
            role: 'assistant',
            text: 'Based on the AI Process, would you like me to generate the architecture diagram?',
            ts: Date.now()
          },
          {
            role: 'user',
            text: 'Yes.',
            ts: Date.now()
          },
          {
            role: 'assistant',
            text: 'Here is your architecture diagram (architecture.png). Click to view.',
            ts: Date.now()
          },

          // Roadmap
          {
            role: 'user',
            text: 'Thanks. I would like to see the features and roadmap.',
            ts: Date.now()
          },
          {
            role: 'assistant',
            text: 'Certainly. The roadmap is being prepared.\n' + 'Click to view the ROADMAP once available.',
            ts: Date.now()
          }
        ]
      }
    ];
  });

  // persist to localStorage on changes
  useEffect(() => {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(allChats));
    } catch (e) {
      // ignore
    }
  }, [allChats]);

  const [activeChatIndex, setActiveChatIndex] = useState<number>(0);
  const [query, setQuery] = useState<string>('');
  const [sidebarOpen, setSidebarOpen] = useState<boolean>(true);
  const [dropdownOpen, setDropdownOpen] = useState<boolean>(true);
  const [showUploadMenu, setShowUploadMenu] = useState<boolean>(false);
  const docInputRef = useRef<HTMLInputElement | null>(null);
  const mediaInputRef = useRef<HTMLInputElement | null>(null);
  const [hoveredChat, setHoveredChat] = useState<number | null>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [isThinking, setIsThinking] = useState(false);
  const authHelper = new AuthHelperService();

  const activeChat = allChats[activeChatIndex];

  // Ensure token is initialized (force getAuthHeader) on mount
  useEffect(() => {
    const initToken = async () => {
      const helper = new (class extends BaseEditPageService<any> {
        constructor() {
          super('chat-auth-init');
        }
      })();

      try {
        await helper.getAuthHeader();
      } catch (err) {
        // Swallow — UI shows errors on requests
        // eslint-disable-next-line no-console
        console.warn('Chatbot token init failed', err);
      }
    };

    initToken();
  }, []);

  /** Supported file types **/
  const allowedDocs = [
    'application/pdf',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'text/csv',
    'image/png',
    'image/jpeg',
    'image/jpg'
  ];
  const allowedMedia = ['audio/mpeg', 'audio/wav', 'video/mp4', 'video/webm', 'video/quicktime', 'video/x-msvideo'];

  const generateChatTitle = (message: string): string => {
    const lower = message.toLowerCase();
    if (lower.includes('api')) return 'API Query Discussion';
    if (lower.includes('project')) return 'Project Planning';
    if (lower.includes('error')) return 'Debugging Session';
    if (lower.includes('data')) return 'Data Analysis';
    if (lower.includes('agentic')) return 'Agentic AI Exploration';
    return message.split(' ').slice(0, 4).join(' ');
  };

  /** Send message (supports text+file or either) **/
  const onSend = async () => {
    // require either text or file
    if ((!query || !query.trim()) && !selectedFile) return;
    if (!activeChat) return;

    setLoading(true);

    const updatedChats = [...allChats];
    const currentChat = { ...updatedChats[activeChatIndex] };

    // ensure session_id exists for this chat
    //if (!currentChat.session_id) currentChat.session_id = chatbotService.generate_random_session_id();

    // create user message entry (for UI history)
    const userMessage: MessageItem = {
      role: 'user',
      text: query?.trim() ? query.trim() : selectedFile ? `Uploaded file: ${selectedFile.name}` : '',
      fileName: selectedFile?.name,
      fileType: selectedFile?.type,
      ts: Date.now()
    };

    currentChat.messages = [...currentChat.messages, userMessage];

    // auto rename if first message
    if (currentChat.messages.length === 1 && currentChat.name === 'New Conversation') {
      currentChat.name = generateChatTitle(userMessage.text || 'Conversation');
    }

    updatedChats[activeChatIndex] = currentChat;
    setAllChats(updatedChats);
    setQuery(''); // clear input in UI

    try {
      setIsThinking(true); // Show typing indicator

      // 1. Fetch dynamic token from backend
      // 1. Fetch dynamic token
      // const headers = await authHelper.getAuthHeader();
      const token = (await authHelper.getAuthHeader()).token; // FIXED ✔

      console.log('Token: ', token);
      // console.log('API ENDPOINT: ', API_END_POINT);
      // console.log('API ENDPOINT: ', process.env.API_END_POINT);
      console.log('API END POINT: ', process.env.REACT_APP_API_END_POINT);
      console.log('Jira Context in Chatbot:', { siteUrl, environmentId, appId });

      const API_END_POINT = process.env.REACT_APP_API_END_POINT;

      // 2. Execute agent
      const response = await chatbotService.executeAgent(token, userMessage.text, API_END_POINT);

      const res = JSON.parse(response.body ?? '{}');
      const data = res ?? null;

      const extractText = (d: any): string => {
        if (!d) return 'No response';

        if (d.message && Array.isArray(d.message.content)) {
          const parts = d.message.content
            .map((c: any) => c.text || '')
            .join('\n')
            .trim();
          if (parts.length > 0) return parts;
        }

        if (typeof d === 'string') return d;
        if (typeof d.text === 'string') return d.text;
        if (typeof d.result === 'string') return d.result;
        if (d.raw && typeof d.raw === 'string') return d.raw;

        try {
          return JSON.stringify(d);
        } catch {
          return 'No response';
        }
      };

      const text = extractText(data);

      setIsThinking(false); // remove typing indicator

      const aiReply: MessageItem = {
        role: 'assistant',
        text,
        ts: Date.now()
      };

      const refreshed = [...updatedChats];
      const refreshedChat = { ...refreshed[activeChatIndex] };
      refreshedChat.messages = [...refreshedChat.messages, aiReply];
      refreshed[activeChatIndex] = refreshedChat;
      setAllChats(refreshed);

      antdMessage.success('Agent executed');
    } catch (err: any) {
      setIsThinking(false);
      const errMsg = err?.message || 'Error executing agent';
      antdMessage.error(errMsg);
      const errReply: MessageItem = { role: 'assistant', text: errMsg, ts: Date.now() };
      const refreshed = [...updatedChats];
      const refreshedChat = { ...refreshed[activeChatIndex] };
      refreshedChat.messages = [...refreshedChat.messages, errReply];
      refreshed[activeChatIndex] = refreshedChat;
      setAllChats(refreshed);
    } finally {
      setLoading(false);
      setSelectedFile(null);
      // clear file inputs (if DOM refs exist)
      if (docInputRef.current) docInputRef.current.value = '';
      if (mediaInputRef.current) mediaInputRef.current.value = '';
    }
  };

  const onNewChat = () => {
    const newChat: Chat = {
      id: Date.now() + Math.floor(Math.random() * 1000),
      name: 'New Conversation',
      messages: []
      //session_id: chatbotService.generate_random_session_id()
    };
    setAllChats((prev) => [newChat, ...prev]);
    setActiveChatIndex(0);
  };

  const handleDeleteChat = (index: number) => {
    setAllChats((prev) => {
      const updated = prev.filter((_, i) => i !== index);
      const newActiveIndex = index === activeChatIndex ? 0 : activeChatIndex;
      setActiveChatIndex(newActiveIndex < updated.length ? newActiveIndex : 0);
      return updated;
    });
  };

  /** File upload logic - docs vs media **/
  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>, type: 'doc' | 'media') => {
    const file = e.target.files?.[0];
    if (!file || !activeChat) return;

    const updatedChats = [...allChats];
    const currentChat = { ...updatedChats[activeChatIndex] };

    if (type === 'doc') {
      if (!allowedDocs.includes(file.type)) {
        antdMessage.warning('Only document or image files are allowed here.');
        currentChat.messages.push({
          role: 'assistant',
          text: `Unsupported file type for document upload: ${file.name}`,
          ts: Date.now()
        });
      } else {
        currentChat.messages.push({
          role: 'user',
          text: `Document uploaded: ${file.name}`,
          fileName: file.name,
          fileType: file.type,
          ts: Date.now()
        });
        setSelectedFile(file);
      }
    } else {
      // media
      if (!allowedMedia.includes(file.type)) {
        antdMessage.warning('Only audio or video files (MP3, WAV, MP4, WEBM, etc.) are allowed here.');
        currentChat.messages.push({
          role: 'assistant',
          text: `Unsupported file type for media upload: ${file.name}`,
          ts: Date.now()
        });
      } else {
        currentChat.messages.push({
          role: 'user',
          text: `Media uploaded: ${file.name}`,
          fileName: file.name,
          fileType: file.type,
          ts: Date.now()
        });
        setSelectedFile(file);
      }
    }

    updatedChats[activeChatIndex] = currentChat;
    setAllChats(updatedChats);
    setShowUploadMenu(false);

    if (type === 'doc' && docInputRef.current) docInputRef.current.value = '';
    if (type === 'media' && mediaInputRef.current) mediaInputRef.current.value = '';
  };

  const handleSelectChat = (index: number) => {
    if (index >= 0 && index < allChats.length) setActiveChatIndex(index);
  };

  return (
    <div className={styles.pageWrapper}>
      {/* Sidebar */}
      <div className={`${styles.sidebar} ${sidebarOpen ? styles.sidebarOpen : styles.sidebarCollapsed}`}>
        <div className={styles.sidebarHeader}>
          {sidebarOpen ? (
            <>
              <h3>Fusefy</h3>
              <Button type="primary" icon={<PlusOutlined />} className={styles.newChatBtn} onClick={onNewChat}>
                New Chat
              </Button>
            </>
          ) : (
            <Tooltip title="New Chat" placement="right">
              <Button
                shape="circle"
                type="primary"
                icon={<PlusOutlined />}
                className={styles.newChatIconOnly}
                onClick={onNewChat}
              />
            </Tooltip>
          )}
        </div>

        {/* Recent Chats */}
        <div className={styles.dropdownSection}>
          {sidebarOpen ? (
            <>
              <div className={styles.dropdownHeader} onClick={() => setDropdownOpen(!dropdownOpen)}>
                <span>Recent Chats</span>
                {dropdownOpen ? (
                  <UpOutlined className={styles.arrowIcon} />
                ) : (
                  <DownOutlined className={styles.arrowIcon} />
                )}
              </div>

              {dropdownOpen && (
                <div className={styles.chatList}>
                  {allChats.map((chat, index) => (
                    <div
                      key={chat.id}
                      className={`${styles.chatItem} ${index === activeChatIndex ? styles.activeChat : ''}`}
                      onMouseEnter={() => setHoveredChat(index)}
                      onMouseLeave={() => setHoveredChat(null)}
                    >
                      <div className={styles.chatInfo} onClick={() => handleSelectChat(index)}>
                        <MessageOutlined className={styles.chatIcon} />
                        <span className={styles.chatTitle}>{chat.name}</span>
                      </div>

                      {hoveredChat === index && (
                        <Tooltip title="Delete Chat">
                          <DeleteOutlined className={styles.deleteIcon} onClick={() => handleDeleteChat(index)} />
                        </Tooltip>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </>
          ) : (
            <Tooltip title="Recent Chats" placement="right">
              <MessageOutlined className={styles.iconOnly} />
            </Tooltip>
          )}
        </div>
      </div>

      {/* Chat Window */}
      <div className={styles.mainArea}>
        <div className={styles.header}>
          <div className={styles.headerLeft}>
            <Button
              type="text"
              icon={<MenuOutlined />}
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className={styles.menuBtn}
            />
            <h2>{activeChat ? activeChat.name : 'Conversation'}</h2>
          </div>
        </div>

        {/* Chat Body */}
        <div className={`${styles.chatBody} ${activeChat && activeChat.messages.length > 0 ? styles.hasMessages : ''}`}>
          {!activeChat || activeChat.messages.length === 0 ? (
            <div className={styles.placeholder}>
              <h3>Welcome to Fusefy AI</h3>
              <p>Start a new conversation to experience Agentic AI.</p>
            </div>
          ) : (
            <>
              {activeChat.messages.map((msg, idx) => (
                <div key={idx} className={msg.role === 'user' ? styles.userMessage : styles.assistantMessage}>
                  {msg.fileName ? (
                    <div>
                      <strong>{msg.fileName}</strong>

                      {msg.text &&
                        msg.text.split('\n').map((line, i) => (
                          <div key={i} style={{ fontSize: 12, color: '#666' }}>
                            {line}
                          </div>
                        ))}
                    </div>
                  ) : (
                    msg.text.split('\n').map((line, i) => <div key={i}>{line}</div>)
                  )}
                </div>
              ))}

              {/* Assistant Thinking Indicator */}
              {isThinking && (
                <div className={styles.assistantMessage}>
                  <div className={styles.typingContainer}>
                    <span className={styles.thinkingLabel}>Assistant is Analyzing</span>
                    <div className={styles.typingDots}>
                      <span>•</span>
                      <span>•</span>
                      <span>•</span>
                    </div>
                  </div>
                </div>
              )}
            </>
          )}
        </div>

        {/* Input Section */}
        <div className={styles.inputArea}>
          <div className={styles.addButtonWrapper}>
            <Button
              shape="circle"
              icon={<PlusOutlined />}
              className={styles.addButton}
              onClick={() => setShowUploadMenu(!showUploadMenu)}
            />
            {showUploadMenu && (
              <div className={styles.uploadMenu}>
                <button className={styles.uploadOption} onClick={() => docInputRef.current?.click()}>
                  <PaperClipOutlined /> Upload Documents
                </button>
                <input
                  type="file"
                  ref={docInputRef}
                  accept=".pdf,.ppt,.pptx,.doc,.docx,.xlsx,.csv,.png,.jpg,.jpeg"
                  style={{ display: 'none' }}
                  onChange={(e) => handleFileSelect(e, 'doc')}
                />
                {/* <button className={styles.uploadOption} onClick={() => mediaInputRef.current?.click()}>
                  Upload Media Files
                </button>
                <input
                  type="file"
                  ref={mediaInputRef}
                  accept="audio/*,video/*,.webm"
                  style={{ display: 'none' }}
                  onChange={(e) => handleFileSelect(e, 'media')}
                /> */}
              </div>
            )}
          </div>

          <Input
            placeholder="Type your query to begin your Agentic AI journey..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onPressEnter={onSend}
            className={styles.searchInput}
          />
          <Button
            type="primary"
            icon={<SendOutlined />}
            onClick={onSend}
            className={styles.sendButton}
            loading={loading}
          />
        </div>
      </div>
    </div>
  );
};

export default Chatbot;
