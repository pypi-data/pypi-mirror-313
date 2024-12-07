<template>
  <div
    :id="`message-${messageData?.id}`"
    v-click-outside="closeEmoji"
    class="ops-message-wrapper"
    :class="{
      'own-message': checkIfMessageMine,
      'admin-message':
        !checkIfMessageMine &&
        checkIfAdminMessage &&
        isClientSupportConversation,
    }"
  >
    <!--  Last previous message time - time label    -->
    <RoomContentDateMessage
      v-if="
        messageIndex === 0 ||
        checkNewDay(
          messageData?.timestamp,
          messages?.[messageIndex - 1]?.timestamp
        )
      "
      :message-time="messageData?.timestamp"
      class="self-center"
    />
    <div
      v-if="
        isNewMessages &&
        messageData?.author.id !== userStore.getUser?.person?.id
      "
      class="ops-message-wrapper__new-message"
    >
      <span>New messages</span>
    </div>
    <div class="ops-message-wrapper__box">
      <VDropdown
        theme="ops-room-item__name"
        :triggers="['hover']"
        :placement="'bottom-start'"
        :distance="-6"
        :disabled="
          !messageData?.author?.details?.first_name &&
          !messageData?.author?.details?.last_name
        "
      >
        <div class="ops-message-wrapper__author">
          <span>{{ messageData?.author?.initials }}</span>
        </div>
        <template #popper>
          <div class="ops-message-wrapper__author-details">
            <span class="ops-message-wrapper__author-details--firstname">
              {{ messageData.author.details.first_name }}
            </span>
            <span class="ops-message-wrapper__author-lastname">
              {{ messageData.author.details.last_name }}
            </span>
          </div>
        </template>
      </VDropdown>
      <div class="group/message ops-message-wrapper__content">
        <div v-if="0" class="ops-message-wrapper__blur" />
        <div
          v-if="0"
          :class="{ 'ops-click !flex': isMenuVisible }"
          class="ops-message-wrapper__actions"
        >
          <OButton
            class="ops-message-wrapper__action"
            prefix-icon="emoji"
            @click="isEmojiVisible = !isEmojiVisible"
          />
          <OMenuHeader
            class="ops-message-wrapper__action ops-message-wrapper__action--arrow"
            icon="arrow"
            :options="menuOptions"
            @click="isMenuVisible = !isMenuVisible"
            @blur="isMenuVisible = false"
          />
        </div>
        <div class="ops-message-wrapper__message ops-message">
          <slot />
          <RoomContentMessageTime :message-data="messageData" />
        </div>
        <RoomReactions
          v-if="0"
          :message-data="messageData"
          :is-emoji-visible="isEmojiVisible"
          @close-emoji="closeEmoji"
        />
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { computed, onMounted, type PropType, ref } from "vue";
import { type IMenuActions, type IMessage } from "@/types/room/room.types";
import RoomContentDateMessage from "@/components/room/content/RoomContentDateMessage.vue";
import OMenuHeader from "@/components/ui/OMenuHeader.vue";
import OButton from "@/components/ui/OButton.vue";
import RoomReactions from "@/components/room/content/RoomReactions.vue";
import RoomContentMessageTime from "@/components/room/content/RoomContentMessageTime.vue";
import { useUserStore } from "@/store/useUserStore";
import type { IRoom } from "@/types/rooms.types";

const userStore = useUserStore();
const emit = defineEmits<{
  (e: "new-message", v: string): void;
}>();
const props = defineProps({
  messages: {
    type: Array as PropType<IMessage[]>,
    default: () => [],
  },
  messageData: {
    type: Object as PropType<IMessage>,
    default: () => ({}),
  },
  messageIndex: {
    type: Number as PropType<number>,
    default: 0,
  },
  isNewMessages: {
    type: Boolean as PropType<boolean>,
    default: false,
  },
  room: {
    type: Object as PropType<IRoom>,
    default: () => ({}),
  },
  isClientSupportConversation: {
    type: Boolean as PropType<boolean>,
    default: false,
  },
});
const menuOptions = ref<IMenuActions[]>([
  { id: "reply", title: "Reply", emitAction: "reply" },
  { id: "editMessage", title: "Edit Message", emitAction: "edit-message" },
  {
    id: "deleteMessage",
    title: "Delete Message",
    emitAction: "delete-message",
  },
]);
const isMenuVisible = ref(false);
const isEmojiVisible = ref(false);

const checkIfMessageMine = computed(
  () => props.messageData?.author.id === userStore.getUser?.person.id
);
const checkIfAdminMessage = computed(() => {
  const isAdminCurrentUser = userStore.getUser?.person.is_staff;
  const isAdminMessage = props.messageData?.author?.is_staff;
  return isAdminCurrentUser && isAdminMessage;
});

const checkNewDay = (current: any, previous: any) => {
  const currentDate = new Date(current).toLocaleDateString();
  const previousDate = new Date(previous).toLocaleDateString();
  return currentDate !== previousDate;
};
const closeEmoji = () => (isEmojiVisible.value = false);

onMounted(() => {
  if (!props.messageData?.is_read) {
    emit("new-message", props.messageData.id);
  }
});
</script>

<style lang="scss">
@mixin message-reverse($bg) {
  @apply items-end ml-auto #{!important};
  .ops-message-wrapper__box {
    @apply flex-row-reverse;

    .ops-message-wrapper__message {
      @apply items-end text-white;
      background-color: $bg;
    }
  }
}
.own-message {
  @include message-reverse(#515d8a);
}
.admin-message {
  @include message-reverse(#9ca3af);
  .ops-message-time__time {
    @apply text-grey-100;
  }
  .ops-message-time__read {
    filter: invert(98%) sepia(3%) saturate(1115%) hue-rotate(181deg)
      brightness(86%) contrast(99%);
  }
}

.ops-message-wrapper {
  @apply w-full rounded-md flex items-start justify-center flex-col;

  &__new-message {
    @apply bg-grey-900 text-white mx-auto rounded-md px-2 py-1 text-xs;
  }

  &__box {
    @apply flex gap-x-2 max-w-[75%] md:max-w-[50%] overflow-hidden;
  }

  &__author {
    @apply bg-white text-xs border border-confetti-500 border-solid rounded-full shrink-0 p-2 w-8 h-8 flex items-center justify-center overflow-hidden cursor-pointer;
  }

  &__author-details {
    @apply text-sm;

    &--firstname {
      @apply mr-1;
    }
  }

  &__content {
    @apply relative overflow-hidden w-full;
  }

  &__message {
    @apply text-grey-900 overflow-hidden w-full;
  }

  &__blur {
    @apply hidden group-hover/message:block blur-[5px] absolute right-2 top-1 bg-confetti-500 w-14 h-6;
  }

  &__actions {
    @apply hidden px-2 py-1 rounded-md absolute z-10 right-0 top-0 bg-confetti-500 justify-end gap-x-1 transition-all duration-200 group-hover/message:flex;
    animation: onHover 0.1s linear;
  }

  &__action {
    @apply w-4 h-4 rounded-full;
    filter: invert(38%) sepia(9%) saturate(2114%) hue-rotate(190deg)
      brightness(92%) contrast(89%);
  }
}

@keyframes onHover {
  from {
    transform: scale(0);
  }
  to {
    transform: scale(1);
  }
}
</style>
