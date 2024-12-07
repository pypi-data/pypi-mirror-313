<template>
  <div class="w-full">
    <span class="header">Attachments</span>
    <div class="table-wrapper">
      <table class="table">
        <thead class="table-head">
          <tr>
            <th class="table-head-cell">File</th>
            <th class="table-head-cell">Description</th>
            <th class="table-head-cell"></th>
          </tr>
        </thead>
        <tbody class="table-body">
          <tr v-for="(attachment, index) in attachments" :key="attachment.id">
            <td class="table-body-cell w-50">
              <div>
                <div v-if="typeof attachment.file === 'string'" class="file-link-wrapper">
                  <a
                    :title="getFilenameByUrl(attachment.file)"
                    class="file-link"
                    :href="attachment.file"
                    target="_blank"
                    >{{ getFilenameByUrl(attachment.file) }}</a
                  >
                </div>
                <input
                  v-else
                  class="table-body-cell-input"
                  type="file"
                  @change="onChangeFile($event, index)"
                />
              </div>
            </td>
            <td class="table-body-cell w-50">
              <input
                class="table-body-cell-input"
                type="text"
                :value="attachment.description"
                @change="onChangeDescription($event, index)"
              />
            </td>
            <td class="table-body-cell">
              <button
                class="btn btn-outline-danger"
                :disabled="isDeleteButtonDisabled"
                @click.stop="onDeleteRow(index)"
              >
                Delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="mt-2">
      <button
        class="btn btn-outline-success btn-sm"
        :disabled="attachments.length >= MAX_ATTACHMENTS"
        @click.stop="onAddRows"
      >
        {{ attachments.length ? 'Add More Attachments' : 'Add Attachments' }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, defineEmits, defineProps, ref, watch } from 'vue';
import { getFilenameByUrl } from '@/helpers/files';

import type { ICrmActivity } from 'shared/types';

const INITIAL_ATTACHMENTS = Array.from({ length: 2 }, () => ({
  id: Date.now(),
  file: null,
  description: ''
}));
const MAX_ATTACHMENTS = 10;

export type TableAttachment = {
  id: number;
  file: File | string | null;
  description: string;
};

export type Attachment<F = File | string> = {
  id: number;
  file: F;
  description: string;
};

type Props = {
  initialAttachments?: ICrmActivity['attachments'];
};

type Emits = {
  (e: 'onDelete', v: TableAttachment): void;
  (e: 'onChange', v: Attachment[]): void;
};

const props = defineProps<Props>();
const emit = defineEmits<Emits>();

const getTableAttachments = (attachments: Props['initialAttachments']): TableAttachment[] => {
  if (!attachments) return INITIAL_ATTACHMENTS;
  return attachments.map((attachment) => ({
    id: attachment?.id ?? Date.now(),
    file: attachment.file ?? null,
    description: attachment.description ?? ''
  }));
};

const attachments = ref<TableAttachment[]>(getTableAttachments(props.initialAttachments));

const isDeleteButtonDisabled = computed(
  () => attachments.value.length === 1 && typeof attachments.value[0].file !== 'string'
);

const onAddRows = () => {
  attachments.value.push({ id: Date.now(), file: null, description: '' });
  if (attachments.value.length < MAX_ATTACHMENTS) {
    attachments.value.push({ id: Date.now(), file: null, description: '' });
  }
};

const onDeleteRow = (rowId: number) => {
  emit('onDelete', attachments.value[rowId]);
  attachments.value.splice(rowId, 1);
};

const onChangeFile = (e: Event, index: number) => {
  const target = e.target as HTMLInputElement;
  const file = target.files?.[0];
  if (file) {
    attachments.value[index].file = file;
  }
};

const onChangeDescription = (e: Event, index: number) => {
  const target = e.target as HTMLInputElement;
  attachments.value[index].description = target.value;
};

watch(
  attachments,
  (attachments) => {
    const filledAttachments = attachments.filter((attachment) => attachment.file) as Attachment[];

    emit('onChange', filledAttachments);
  },
  { deep: true }
);
</script>

<style scoped lang="scss">
.header {
  display: inline-block;
  background-color: #515d8a;
  border-radius: 0.3rem;
  font-size: 1rem;
  font-weight: 500;
  padding-top: 0.5rem;
  padding-bottom: 0.5rem;
  padding-right: 1rem;
  padding-left: 1rem;
  margin-bottom: 0.25rem;
  line-height: 1;
  color: #fff;
  white-space: nowrap;
  vertical-align: baseline;
  width: 100%;
}

.table-wrapper {
  font-size: 1rem;
  font-weight: 400;
  line-height: 1.5;
  color: #374151;
  overflow-x: auto;
}

.table {
  --bs-table-bg: transparent;
  width: 100%;
  margin-bottom: 1rem;
  color: #374151;
  vertical-align: top;
  border-color: #e5e7eb;
  caption-side: bottom;
  margin-bottom: 0;

  &-head {
    vertical-align: bottom;

    &-cell {
      border: none;
      background-color: #f2f4f6;
      color: #515d8a;
      padding-top: 0.75rem;
      padding-bottom: 0.75rem;
      font-size: 0.75rem;
      text-transform: uppercase;
      font-weight: 600;
    }
  }

  &-body {
    &-cell {
      font-size: 0.875rem;
      white-space: nowrap;
      background-color: var(--bs-table-bg);
      padding: 0.25rem;
      border: none;

      &-input {
        display: block;
        width: 100%;
        padding: 0.5rem 1rem;
        font-size: 0.875rem;
        font-weight: 400;
        line-height: 1.5;
        color: #6b7280;
        background-color: #fff;
        background-clip: padding-box;
        border: 0.0625rem solid #d1d5db;
        -webkit-appearance: none;
        appearance: none;
        border-radius: 0.5rem;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.07);
        transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
        overflow: hidden;

        &:focus {
          color: #6b7280;
          background-color: #fff;
          border-color: #98a1c3;
          outline: 0;
          box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.07), 0 0 0 0.18rem rgba(81, 93, 138, 0.25);
        }

        &:not(:disabled):not([readonly]) {
          cursor: pointer;
        }

        &:hover:not(:disabled):not([readonly])::file-selector-button {
          background-color: #f2f2f2;
        }

        &::file-selector-button {
          font: inherit;
          padding: 0.5rem 1rem;
          margin: -0.5rem -1rem;
          -webkit-margin-end: 1rem;
          margin-inline-end: 1rem;
          color: #6b7280;
          background-color: #fff;
          pointer-events: none;
          border-color: inherit;
          border-style: solid;
          border-width: 0;
          border-inline-end-width: 0.0625rem;
          border-radius: 0;
          transition: color 0.15s ease-in-out, background-color 0.15s ease-in-out,
            border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
        }
      }
    }
  }
}

.btn {
  display: inline-block;
  font-weight: 500;
  line-height: 1.5;
  color: #374151;
  text-align: center;
  vertical-align: middle;
  cursor: pointer;
  -webkit-user-select: none;
  user-select: none;
  background-color: transparent;
  border: 0.0625rem solid transparent;
  border-top-color: transparent;
  border-right-color: transparent;
  border-bottom-color: transparent;
  border-left-color: transparent;
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
  border-radius: 0.5rem;
  transition: color 0.15s ease-in-out, background-color 0.15s ease-in-out,
    border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
  -webkit-appearance: button;

  &:disabled {
    pointer-events: none;
    opacity: 0.65;
    box-shadow: none;
  }

  &-outline-danger {
    color: #e11d48;
    border-color: #e11d48;

    &:hover,
    &:active {
      color: #fff;
      background-color: #e11d48;
      border-color: #e11d48;
    }

    &:focus {
      box-shadow: 0 0 0 0.18rem rgba(225, 29, 72, 0.5);
    }

    &:active:focus {
      box-shadow: inset 0 3px 5px rgba(17, 24, 39, 0.125), 0 0 0 0.18rem rgba(225, 29, 72, 0.5);
    }

    &:disabled {
      color: #e11d48;
      background-color: transparent;
    }
  }

  &-outline-success {
    color: #10b981;
    border-color: #10b981;

    &:hover,
    &:active {
      color: #111827;
      background-color: #10b981;
      border-color: #10b981;
    }

    &:focus {
      box-shadow: 0 0 0 0.18rem rgba(16, 185, 129, 0.5);
    }

    &:active:focus {
      box-shadow: inset 0 3px 5px rgba(17, 24, 39, 0.125), 0 0 0 0.18rem rgba(16, 185, 129, 0.5);
    }

    &:disabled {
      color: #10b981;
      background-color: transparent;
    }
  }

  &-sm {
    padding: 0.375rem 0.625rem;
    font-size: 0.875rem;
    border-radius: 0.5rem;
  }

  &::-moz-focus-inner {
    padding: 0;
    border-style: none;
  }

  &:not(:disabled) {
    cursor: pointer;
  }
}

.file-link-wrapper {
  text-wrap: nowrap;
  text-overflow: ellipsis;
  overflow: hidden;
  max-width: 275px;

  .file-link {
    color: #3b82f6;
    text-decoration: underline;

    &:hover {
      color: #2563eb;
    }
  }
}
</style>
