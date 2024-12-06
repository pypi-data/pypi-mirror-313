<template>
  <div :class="$style['ops-room-header']">
    <div :class="$style['ops-room-header__wrapper']">
      <button
        v-if="!headlessModId"
        :class="[
          $style['ops-room-header__button'],
          $style['ops-room-header__button--desktop'],
          { [$style['ops-room-header__button--rotate']]: !showRoomsList },
        ]"
        @click="$emit('toggleRoomsList')"
      >
        <img :src="getImageUrl('assets/icons/toggle.svg')" alt="toggle icon" />
      </button>
      <button
        v-if="!headlessModId"
        :class="[
          $style['ops-room-header__button'],
          $style['ops-room-header__button--mobile'],
        ]"
        @click="toggleMobile"
      >
        <img :src="getImageUrl('assets/icons/toggle.svg')" alt="toggle icon" />
      </button>
      <div :class="$style['ops-info-wrapper']">
        <div :class="$style['ops-text-ellipsis']">
          <a
            v-if="room?.header_url"
            :class="[
              $style['ops-info-wrapper__name'],
              $style['ops-text-ellipsis'],
            ]"
            :href="room?.header_url"
            target="_blank"
          >
            <span>{{ room.name }}</span>
            <img
              :class="$style['ops-info-wrapper__link']"
              :src="getImageUrl('assets/icons/link.svg')"
              alt="link"
            />
          </a>
          <p
            v-else
            :class="[
              $style['ops-info-wrapper__name'],
              $style['ops-text-ellipsis'],
            ]"
          >
            {{ room.name }}
          </p>
          <div
            :class="[
              $style['ops-info-wrapper__info'],
              $style['ops-text-ellipsis'],
            ]"
          >
            <RoomHeaderStatus>
              <template #trigger>
                <span class="cursor-pointer">{{ userStatus }}</span>
              </template>
            </RoomHeaderStatus>
          </div>
        </div>
      </div>
    </div>
    <RoomUserAction
      v-if="websocketService.loadingOptions.value.isLoaded"
      :room="room"
    />
  </div>
</template>

<script setup lang="ts">
import { computed, type PropType } from "vue";
import { getImageUrl } from "@/helpers/import-image";
import type { IRoom } from "@/types/rooms.types";
import { useUserStore } from "@/store/useUserStore";
import websocketService from "@/services/chat/websocket-chat";
import { useMainStore } from "@/store/useMainStore";
import { removeOwnIdOnline } from "@/helpers/general";
import RoomUserAction from "@/components/room/header/RoomUserAction.vue";
import RoomHeaderStatus from "@/components/room/header/RoomHeaderStatus.vue";

const mainStore = useMainStore();
const userStore = useUserStore();
const props = defineProps({
  room: {
    type: Object as PropType<IRoom>,
    default: null,
  },
  userStatus: {
    type: String,
    default: "online",
  },
  typingUsers: {
    type: Boolean,
    default: false,
  },
  showRoomsList: {
    type: Boolean,
    default: true,
  },
});

defineEmits<{
  (e: "toggleRoomsList"): void;
}>();

const headlessModId = computed(() => websocketService.headlessModeId.value);
const userTyping = computed(() => websocketService.userTyping.value);

const checkOwnChat = computed(() => {
  return userTyping.value.conversation_id === props.room?.id;
});

const currentUsersOnline = computed(() =>
  removeOwnIdOnline(websocketService.peopleOnline.value)
);
const totalUsersIdInRoom = computed(() =>
  removeOwnIdOnline(websocketService.peopleInRoom.value.map((el) => el?.id))
);
const filterUserOnline = computed(() => {
  const currentRoomOnline = currentUsersOnline.value.filter((el: number) =>
    totalUsersIdInRoom.value.includes(el)
  );
  return `online (${currentRoomOnline?.length}/${totalUsersIdInRoom.value?.length})`;
});

const userStatus = computed(() => {
  return userTyping.value?.person?.id &&
    userTyping.value?.person?.id !== userStore.getUser?.person?.id &&
    checkOwnChat.value
    ? `${userTyping.value.person.details?.first_name} typing...`
    : filterUserOnline.value;
});

const toggleMobile = () => {
  mainStore.toggleMobileVisible();
};
</script>
<style lang="scss" module>
//header
.ops-room-header {
  @apply flex items-center w-full h-[4rem] z-[10] mr-[1px] border-b-[1px] border-grey-100 border-solid bg-white px-3 #{!important};

  &__button {
    @apply cursor-pointer mr-[0.9rem] max-h-[1.875rem] hover:opacity-70 transition-all duration-200 #{!important};

    &--desktop {
      @apply hidden md:flex #{!important};
    }

    &--mobile {
      @apply flex md:hidden #{!important};
    }

    &--rotate {
      transform: rotateY(180deg);
    }
  }

  .ops-room-header__wrapper {
    @apply flex items-center min-w-0 h-full w-full py-0 pr-4;
  }

  .ops-info-wrapper {
    @apply flex items-center w-full h-full min-w-0;

    &__name {
      @apply font-medium text-[1rem] leading-6 text-grey-900 cursor-pointer #{!important};
    }

    &__link {
      @apply w-4 h-4 ml-2;
      filter: invert(34%) sepia(8%) saturate(2691%) hue-rotate(190deg)
        brightness(97%) contrast(80%);
    }

    &__info {
      @apply leading-5 text-[0.8rem] text-grey-200;
    }
  }
}
</style>
