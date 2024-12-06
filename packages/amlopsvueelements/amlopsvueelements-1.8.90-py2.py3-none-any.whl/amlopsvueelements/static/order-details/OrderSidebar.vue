<template>
  <div class="order-sidebar flex h-full" :class="{ 'is-sidebar-closed': isSidebarClosed }">
    <div
      class="order-sidebar-wrap flex bg-white rounded-md"
      :style="{ height: calculateMaxHeight() }"
    >
      <div class="order-sidebar-content w-full flex flex-col">
        <div
          v-show="activeTab?.name !== 'Chat'"
          class="order-sidebar-content-header px-[0.75rem] py-[0.5rem] flex justify-between items-center"
        >
          {{ activeTab?.name }}
          <Button
            v-if="activeTab?.name === 'Notes'"
            class="button flex items-center gap-2"
            @click="isAddingNote = true"
          >
            <img src="../../assets/icons/plus.svg" alt="add" />
            Add Note
          </Button>
        </div>
        <ScrollBar class="grow" :class="{ 'my-[0.75rem]': activeTab?.name !== 'Chat' }">
          <div
            v-if="activeTab?.name === 'Notes'"
            class="order-sidebar-content-data px-[0.75rem] flex flex-col gap-3 max-h-full"
          >
            <Notes :is-adding-note="isAddingNote" @close-adding-note="onCloseAddingNote" />
          </div>
          <div v-show="activeTab?.name === 'Chat'" class="order-sidebar-content-data">
            <Chat :is-open="activeTab?.name === 'Chat'" />
          </div>
          <div v-if="activeTab?.name === 'Activity'" class="order-sidebar-content-data">
            <ActivityLog />
          </div>
        </ScrollBar>
      </div>
      <div class="order-sidebar-menu w-2/12 py-[1rem] px-[0.75rem] flex flex-col gap-4">
        <div
          v-for="el in sidebar"
          :key="el.name"
          class="order-sidebar-menu-el flex flex-col items-center"
          :class="{ active: activeTab?.name === el.name }"
          @click="changeTab(el)"
        >
          <div
            class="img-wrap flex items-center justify-center p-[0.5rem] border-0 rounded-lg relative"
          >
            <div
              v-if="el.name === 'Chat' && unreadMessagesCount > 0"
              class="unread-messages-badge absolute w-[20px] h-[20px] top-[-0.25rem] right-[-0.25rem] flex items-center justify-center"
            >
              {{ unreadMessagesCount }}
            </div>
            <img :src="getImageUrl(`assets/icons/${el.icon}.svg`)" :alt="el.icon" />
          </div>
          {{ el.name }}
        </div>

        <div
          class="close-sidebar img-wrap cursor-pointer flex items-center justify-center p-[0.5rem]"
          :class="{ 'is-closed': isSidebarClosed }"
          @click="changeSidebar"
        >
          <img src="../../assets/icons/sidebar-close.svg" alt="sidebar_close" />
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, onUnmounted, type PropType, ref } from 'vue';
import { watch } from 'vue';
import type { BaseValidation } from '@vuelidate/core';
import { Button } from 'shared/components';
import { getImageUrl } from '@/helpers';
import { ActivityLog, Chat, Notes } from '../datacomponent';
import ScrollBar from '../forms/ScrollBar.vue';

import type { IOrder } from 'shared/types';

type Tab = {
  name: string;
  icon: string;
};

const props = defineProps({
  validationInfo: {
    type: Object as PropType<BaseValidation>,
    default: () => null
  },
  isLoading: {
    type: Boolean as PropType<boolean>,
    default: false
  },
  order: {
    type: Object as PropType<IOrder>,
    default: null
  },
  headerHeight: {
    type: Number,
    default: 0
  }
});

const sidebar: Tab[] = [
  { name: 'Notes', icon: 'notes' },
  { name: 'Chat', icon: 'chat' },
  { name: 'Activity', icon: 'activity' }
];

const activeTab = ref<null | Tab>(null);
const isSidebarClosed = ref(true);
const isAddingNote = ref(false);

const unreadMessagesCount = ref(0);

function onCloseAddingNote() {
  isAddingNote.value = false;
}

function changeTab(el: any) {
  isAddingNote.value = false;

  if (activeTab.value?.name === el.name) {
    isSidebarClosed.value = !isSidebarClosed.value;
  } else {
    isSidebarClosed.value = false;
  }
  activeTab.value = el;
}

const changeSidebar = () => {
  isAddingNote.value = false;
  activeTab.value = isSidebarClosed.value && !activeTab.value ? sidebar[0] : null;
  isSidebarClosed.value = !isSidebarClosed.value;
};

const calculateMaxHeight = () => {
  let height = '100vh - 6rem';
  if (props.headerHeight > 17) {
    height = `calc(100vh - ${props.headerHeight}px - 6rem)`;
    window.chat_max_height = `calc(100vh - ${props.headerHeight}px - 6rem)`;
  } else {
    window.chat_max_height = '100vh - 6rem';
  }
  return height;
};

watch(
  () => props.headerHeight,
  () => {
    calculateMaxHeight();
  }
);

onMounted(() => {
  setTimeout(() => {
    window.chat_unread_messages_subject?.subscribe((value) => {
      unreadMessagesCount.value = value;
    });
  }, 2000);
});

onUnmounted(() => {
  window.chat_unread_messages_subject?.unsubscribe();
});
</script>

<style lang="scss">
.button {
  background-color: rgba(81, 93, 138, 1) !important;
  color: white !important;
  font-weight: 500 !important;
  font-size: 16px !important;
  @apply flex shrink-0 focus:shadow-none mb-0 mt-0 p-[0.5rem] px-4 rounded-lg #{!important};
}

.order-sidebar {
  justify-content: flex-end;
  width: 35%;

  &-wrap {
    width: 100%;
    border: 1px solid transparent;
  }

  &-content {
    &-header {
      font-size: 18px;
      font-weight: 600;
      color: theme('colors.main');
      border-bottom: 1px solid theme('colors.dark-background');
      min-height: 3.5rem;
    }

    &-data {
      height: 100%;
      max-height: 460px;
      // overflow-y: auto;

      &-activity {
        &:first-of-type {
          .order-activity-info-side {
            padding-top: 12px;
          }

          .line-top {
            display: none;
          }
        }

        &:last-of-type {
          .line-bottom {
            display: none;
          }
        }

        .order-activity-info {
          position: relative;

          &-name {
            color: rgba(39, 44, 63, 1);
            font-weight: 600;
            font-size: 14px;
          }

          &-date {
            color: rgba(133, 141, 173, 1);
            font-weight: 400;
            font-size: 12px;
          }

          &-side {
            .circle {
              height: 8px;
              width: 8px;
              background-color: rgba(255, 255, 255, 1);
              border: 2px solid rgba(125, 148, 231, 1);
              border-radius: 50%;
              left: -1rem;
            }

            .line-bottom {
              width: 1px;
              background-color: rgba(223, 226, 236, 1);
              border: 1px solid rgba(223, 226, 236, 1);
              height: 100%;
              top: 6px;
              left: 1.5px;
            }

            .line-top {
              width: 1px;
              background-color: rgba(223, 226, 236, 1);
              border: 1px solid rgba(223, 226, 236, 1);
              height: 12px;
              top: 6px;
              left: 1.5px;
            }
          }
        }

        .order-activity-data {
          color: rgba(39, 44, 63, 1);
          font-weight: 400;
          font-size: 15px;
        }
      }
    }
  }

  &.is-sidebar-closed {
    width: 73px;

    .order-sidebar-content {
      display: none;
      transition: 0.5s;
    }

    .order-sidebar-menu {
      width: 100%;
    }

    .order-sidebar-wrap {
      width: fit-content;
    }
  }

  &-menu {
    position: relative;
    border-left: 1px solid theme('colors.dark-background');
    max-width: 73px;

    &-el {
      color: theme('colors.main');
      font-size: 14px;
      font-weight: 500;
      cursor: pointer;

      .img-wrap {
        width: 40px !important;
        height: 40px !important;

        .unread-messages-badge {
          background-color: #e11d48;
          color: white;
          font-size: 10px;
          border-radius: 50%;
        }
      }

      img {
        width: 20px !important;
        height: 20px !important;
      }

      &.active {
        color: rgba(81, 93, 138, 1);

        .img-wrap {
          background-color: rgba(125, 148, 231, 0.1);
        }
      }
    }

    .close-sidebar {
      position: absolute;
      width: 100%;
      bottom: 1rem;
      left: 0;

      &.is-closed {
        transform: rotate(180deg);
      }
    }
  }
}
</style>
