<template>
  <div>
    <p
      v-if="firstParticipant?.id === roomData?.id"
      :class="$style['ops-rooms-item-other-conversations']"
    >
      Other Conversations
    </p>
    <div
      v-if="roomData?.id"
      :class="[
        $style['ops-rooms-item'],
        { [$style['ops-rooms-item__selected']]: isSelectedRoom },
      ]"
      @click.stop="onSelectRoom"
    >
      <div :class="[$style['ops-rooms-item__content'], $style['content']]">
        <div :class="$style['content__info']">
          <VDropdown
            theme="ops-room-item__name"
            :triggers="['hover']"
            :placement="'bottom-start'"
            :distance="6"
          >
            <h2 :class="$style['title']">{{ roomData?.name }}</h2>
            <template #popper>
              <h2 :class="$style['title']">{{ roomData?.name }}</h2>
            </template>
          </VDropdown>
          <p
            v-if="roomData.latest_message_text"
            :class="$style['content__last-message']"
          >
            {{ roomData?.latest_message_text }}
          </p>
        </div>
        <div :class="[$style['ops-rooms-item__action'], $style['action']]">
          <p
            v-if="roomData?.latest_message_timestamp"
            :class="$style['action__time']"
          >
            {{ formatDate }}
          </p>
          <transition name="ops-slide-left">
            <div
              v-if="roomData?.unread_messages"
              :class="$style['ops-rooms-item__unread-message']"
            >
              <span>{{ formatUnreadMessages }}</span>
            </div>
          </transition>
        </div>
      </div>
      <OMenuHeader
        v-if="roomData?.is_deletable"
        :options="menuOptions"
        class="w-4 absolute right-1"
        @delete-room="onDeleteRoom"
      />
    </div>
  </div>
</template>

<script lang="ts" setup>
import { computed, type PropType, ref } from "vue";
import type { IRoom } from "@/types/rooms.types";
import dayjs from "dayjs";
import relativeTime from "dayjs/plugin/relativeTime";
import isToday from "dayjs/plugin/isToday";
import websocketService from "@/services/chat/websocket-chat";
import websocketChat from "@/services/chat/websocket-chat";
import OMenuHeader from "@/components/ui/OMenuHeader.vue";
import type { IMenuActions } from "@/types/room/room.types";
import chatService from "@/services/chat/chat";

dayjs.extend(relativeTime);
dayjs.extend(isToday);
const props = defineProps({
  roomData: {
    type: Object as PropType<IRoom>,
    default: () => ({}),
  },
  isSelectedRoom: {
    type: Boolean,
    default: false,
  },
  index: {
    type: Number as PropType<number>,
    default: 0,
  },
  firstParticipant: {
    type: Object as PropType<IRoom>,
    default: null,
  },
});

const emit = defineEmits(["select-room"]);

const menuOptions = ref<IMenuActions[]>([
  { id: "deleteRoom", title: "Delete Room", emitAction: "delete-room" },
]);

const isLoading = computed(() => websocketService.loadingOptions.value.loading);
const formatDate = computed(() =>
  dayjs(props.roomData?.latest_message_timestamp).isToday()
    ? dayjs().to(props.roomData?.latest_message_timestamp)
    : dayjs(props.roomData?.latest_message_timestamp).format("DD-MM-YYYY")
);
const formatUnreadMessages = computed(() =>
  props.roomData.unread_messages >= 100 ? "99+" : props.roomData.unread_messages
);

const onSelectRoom = () => {
  if (
    !isLoading.value &&
    websocketChat.selectedRoom.value?.id !== props.roomData?.id
  ) {
    emit("select-room", props.roomData);
  }
};

const onDeleteRoom = async () => {
  const { isConfirmed } = await window.Swal({
    title: "Delete Room",
    text: "Deleting room, you will fully delete history of this room",
    icon: "info",
    showCancelButton: true,
  });
  if (isConfirmed && props.roomData?.id) {
    await chatService.deleteConversation(props.roomData?.id);
  }
};
</script>

<style lang="scss" module>
.ops-rooms-item-other-conversations {
  @apply text-center mb-2 bg-confetti-800 rounded-md text-sm text-grey-800 font-medium #{!important};
}

.ops-rooms-item {
  @apply min-h-[5.5rem] relative mx-0.5 cursor-pointer flex p-4 rounded-lg mb-2 text-grey-900 hover:outline hover:outline-1 hover:outline-confetti-500;

  &__selected {
    @apply bg-confetti-500;
  }

  .content {
    @apply w-full overflow-hidden mr-2;

    &__info {
      @apply w-full overflow-hidden mr-2 flex flex-col justify-between;
      .title {
        @apply text-sm text-grey-900 font-medium truncate inline-block w-full #{!important};
      }
    }

    &__last-message {
      @apply text-[0.75rem] leading-5 truncate text-grey-200;
    }

    .action {
      @apply flex justify-between;

      &__time {
        @apply text-[0.68rem] leading-[1.2rem] truncate text-grey-200;
      }
    }
  }

  &__unread-message {
    @apply px-1 bg-grey-900 flex items-center justify-center text-white text-[0.7rem] text-center rounded-full min-w-[1.25rem];
  }
}

@keyframes scaleDown {
  0% {
    transform: scale(1);
  }
  25% {
    transform: scale(0.95);
  }
  50% {
    transform: scale(1);
  }
  75% {
    transform: scale(0.98);
  }
  100% {
    transform: scale(1);
  }
}
</style>
<!-- styles for floating-vue package -->
<style lang="scss">
.v-popper--theme-ops-room-item__name {
  .v-popper__inner {
    @apply bg-white rounded-md px-2 py-1 border-[1px] border-grey-900 border-solid text-grey-900 #{!important};
    h2 {
      @apply text-sm my-0 font-normal;
    }
  }

  .v-popper__arrow-container {
    .v-popper__arrow-outer {
      @apply border-grey-900 border-solid;
    }
  }
}
</style>
