import { useDebounceFn } from "@vueuse/core";
import websocketService from "@/services/chat/websocket-chat";
import { WS_TYPES } from "@/types/general.types";
import { useSendMessage } from "@/composables/useSendMessage";
import { useConversationDetails } from "@/composables/useConversationDetails";
import { scrollToBottom } from "@/helpers/scroll";

import { useMainStore } from "@/store/useMainStore";
import { getChatModeId } from "@/helpers/general";
import { soundNotify } from "@/helpers/sound-notification";
import type { IMessage } from "@/types/room/room.types";

/**
 * global vars for current file
 **/
const globalVar = {
  timer: 0,
};

/**
 * Methods remove current user id from users - for displaying total online users
 * @users - list of online users
 **/

const peopleOnline = (users: number[]) => {
  websocketService.peopleOnline.value = users;
};

const onUserSettingsUpdate = (settings: any) => {
  websocketService.userSettings.value = settings;
};

/**
 * Methods which called when "chat_messages" signal was called
 * @message - current message
 **/
const sendMessage = async (message: any) => {
  const {
    ownMessage,
    pushUnreadMessage,
    addFakeMessageForRerender,
    pushMessagesIntoCurrentRoom,
    setDelayOnMessage,
  } = useSendMessage(message);

  if (!ownMessage.value && !message.is_read) {
    pushUnreadMessage();
  }
  if (message.conversation === websocketService.selectedRoom.value?.id) {
    await pushMessagesIntoCurrentRoom();
    await addFakeMessageForRerender();
    await setDelayOnMessage();
  }
  if (!websocketService.isUserInConversation.value) {
    setTimeout(() => {
      scrollToBottom(".vue-recycle-scroller");
    }, 0);
  }
};

/**
 * Methods which called when "conversation_details" signal was called
 * @conversation - info about current conversation
 **/
const onConversationDetails = async (conversation: any) => {
  const { conversationAction, updateRoomInList } =
    useConversationDetails(conversation);

  await conversationAction();

  if (!getChatModeId()) {
    await updateRoomInList(conversation);
  }
};

/**
 * Methods which called when "chat_message_update" signal was called
 * @message - updated message
 **/
const chatMessageUpdate = (message: any) => {
  const findCurrentMessageIndex = websocketService.messages.value.findIndex(
    (el) => el.id === message.id
  );
  websocketService.messages.value[findCurrentMessageIndex] = message;
  clearTimeout(globalVar.timer);
  globalVar.timer = setTimeout(() => {
    websocketService.unreadMessages.value = [];
  }, 3000);
};
const recentMessages = (tick: any) => {
  websocketService.messages.value = tick.messages;
  websocketService.hasMoreMessages.value = tick.has_more;
  websocketService.unreadMessages.value = tick.messages
    .filter((el: IMessage) => !el?.is_read)
    .map((el: IMessage) => el?.id);
  websocketService.loadingOptions.value.loading = false;
  websocketService.loadingOptions.value.isLoaded = true;
};

const onConversationDelete = async (id: string) => {
  const mainStore = useMainStore();
  mainStore.setDeletedIdChat(id);
  await websocketService.loadRooms();
};

const invalidateTypingState = useDebounceFn(() => {
  websocketService.userTyping.value = {};
}, 3200);

/**
 * Methods call when some of websocket signal was called
 * @tick - current signal data
 **/
export const websocketMessages = (tick: any) => {
  switch (true) {
    case WS_TYPES.PEOPLE_ONLINE === tick.type:
      peopleOnline(tick.message);
      break;
    case WS_TYPES.USER_SETTINGS === tick.type:
      onUserSettingsUpdate(tick.settings);
      break;
    case WS_TYPES.RECENT_MESSAGES === tick.type:
      recentMessages(tick);
      break;
    case WS_TYPES.CHAT_MESSAGES === tick.type:
      sendMessage(tick.message);
      break;
    case WS_TYPES.TYPING === tick.type && tick.typing:
      websocketService.userTyping.value = tick;
      invalidateTypingState();
      break;
    case WS_TYPES.CHAT_MESSAGE_UPDATE === tick.type:
      chatMessageUpdate(tick.message);
      break;
    case WS_TYPES.CONVERSATION_DETAILS === tick.type:
      onConversationDetails(tick.conversation);

      if (tick.conversation.unread_messages) {
        soundNotify();
      }

      break;
    case WS_TYPES.CONVERSATION_DELETE === tick.type:
      onConversationDelete(tick.conversation_id);
      break;
  }
};
