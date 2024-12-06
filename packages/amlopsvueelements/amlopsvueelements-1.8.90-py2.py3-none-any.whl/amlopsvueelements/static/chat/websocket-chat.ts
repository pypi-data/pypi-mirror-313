import { ref } from "vue";
import { type IMessage } from "@/types/room/room.types";
import { websocketMessages } from "@/helpers/websocket-messages";
import {
  getChatApiToken,
  getWebSocketBaseUrl,
  getChatConversationGroupId,
} from "@/helpers/general";
import { type IPeople, type IRoom } from "@/types/rooms.types";
import chatService from "@/services/chat/chat";
import { WS_CONNECTION } from "@/types/general.types";
import { useMainStore } from "@/store/useMainStore";

class websocketService {
  // global variables
  public socket = ref<any>();
  public rooms = ref<IRoom[]>([]);
  public messages = ref<IMessage[]>([]);
  public peopleOnline = ref<number[]>([]);
  public userSettings = ref<any>({});
  public userTyping = ref<any>({});
  public unreadMessages = ref<string[]>([]);
  public selectedRoom = ref<IRoom>({} as IRoom);
  public hasMoreMessages = ref(false);
  public headlessModeId = ref("");
  public isUserInConversation = ref(false);
  public loadingOptions = ref({
    loading: false,
    isLoaded: false,
    roomsLoading: false,
  });
  public peopleInRoom = ref<IPeople[]>([]);
  public onErrorSocket = ref(false);
  public socketState = ref(0);

  // local variables
  private reconnectCounter = 0;
  openSocket = async (id: string) => {
    this.loadingOptions.value.loading = true;

    if (this.socket.value) {
      this.socket.value.onclose = undefined;
      this.socket.value.close();
    }

    this.socket.value = new WebSocket(
      import.meta.env.DEV
        ? `${getWebSocketBaseUrl()}/chat/ws/${id}/?token=${getChatApiToken()}`
        : `${getWebSocketBaseUrl()}/chat/ws/${id}/`
    );
    this.socket.value.onopen = (event: any): void => {
      console.log("SOCKET IS OPEN WITH MESSAGE", event);
      this.onErrorSocket.value = false;
      this.setSocketState(event);
      this.resetReconnectCounter();
    };

    this.socket.value.onmessage = (event: MessageEvent) => {
      console.log("SOCKET MESSAGE", JSON.parse(event.data));
      const currentTick = JSON.parse(event.data);
      websocketMessages(currentTick);
    };

    this.socket.value.onerror = (event: any) => {
      this.loadingOptions.value.loading = false;
      this.setSocketState(event);
    };

    this.socket.value.onclose = (event: MessageEvent) => {
      console.log("SOCKET MESSAGE", event);
      this.loadingOptions.value.isLoaded = false;
      this.setSocketState(event);
      this.reconnectToSocket();
    };
  };

  closeSocket = () => {
    this.socket.value?.close();
    useMainStore().setDeletedIdChat(null);
    this.loadingOptions.value.isLoaded = false;
  };
  sendMessage = (message: any) => {
    try {
      this.socket.value?.send(JSON.stringify(message));
    } catch (e: any) {
      throw new Error(e);
    }
  };

  fetchRoom = async (id: string) => {
    this.selectedRoom.value = await chatService.fetchConversationDetail(id);
    await this.openSocket(id);
  };

  loadRooms = async () => {
    try {
      this.loadingOptions.value.roomsLoading = true;
      const chatConversationGroupId = getChatConversationGroupId();
      if (!chatConversationGroupId)
        this.rooms.value = await chatService.fetchConversations();
      else
        this.rooms.value = await chatService.fetchConversationsGroup(
          chatConversationGroupId
        );
      this.loadingOptions.value.roomsLoading = false;
    } catch (e: any) {
      this.loadingOptions.value.roomsLoading = false;
      throw new Error(e);
    } finally {
      this.loadingOptions.value.roomsLoading = false;
    }
  };

  reconnectToSocket = async (): Promise<void> => {
    setTimeout(async (): Promise<void> => {
      if (this.reconnectCounter <= 5) {
        await this.openSocket(this.selectedRoom.value?.id);
      } else {
        this.onErrorSocket.value = true;
      }
      this.reconnectCounter++;
    }, 2000);
  };

  waitForConnection = (callback: any, interval: number) => {
    if (this.socket.value.readyState === WS_CONNECTION.OPEN) {
      callback();
      this.onErrorSocket.value = false;
    } else {
      setTimeout(() => {
        this.waitForConnection(callback, interval);
      }, interval);
    }
  };

  setSocketState = (event: any) => {
    this.socketState.value = event.target.readyState;
  };

  resetReconnectCounter = () => (this.reconnectCounter = 0);
}

export default new websocketService();
