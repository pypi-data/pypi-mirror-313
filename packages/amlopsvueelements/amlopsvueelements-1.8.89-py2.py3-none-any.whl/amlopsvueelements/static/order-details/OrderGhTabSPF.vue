<template>
  <div class="w-full h-auto flex flex-col gap-2">
    <div class="spf-step bg-white w-full border border-transparent rounded-md">
      <div class="spf-step-header flex justify-between py-[1rem] px-[0.75rem]">
        <div class="spf-step-header-name">Services Provided Form</div>
        <div class="loading-wrap">
          <Loading v-if="false" />
        </div>
      </div>
      <div v-if="true" class="spf-step-content">
        <div class="spf-step-content-header-sub flex">
          <div class="spf-step-content-header-sub-wrap flex w-5/12 py-[0.5rem] pl-[0.75rem] gap-2">
            <div class="spf-step-content-header-sub-el flex w-full justify-start">Name</div>
          </div>
          <div class="spf-step-content-header-sub-wrap flex w-1/12 py-[0.5rem] pl-[0.75rem]">
            <div class="spf-step-content-header-sub-el flex w-full justify-center">
              Is Pre-Ticked
            </div>
          </div>
          <div class="spf-step-content-header-sub-wrap flex w-1/12 py-[0.5rem] pl-[0.75rem]">
            <div class="spf-step-content-header-sub-el flex w-full justify-center">Was Taken</div>
          </div>
          <div class="spf-step-content-header-sub-wrap flex w-5/12 py-[0.5rem] pl-[0.75rem]">
            <div class="spf-step-content-header-sub-el flex w-full justify-start">Comments</div>
          </div>
        </div>
        <div
          v-for="(service, index) in mockServices"
          :key="index"
          class="spf-step-content-element flex"
        >
          <div
            class="spf-step-content-element-wrap flex w-5/12 py-[0.5rem] pl-[0.75rem] el-border-light gap-2"
          >
            <div class="spf-step-content-element-el-name flex justify-start items-center w-6/12">
              {{ service.name }}
            </div>
          </div>
          <div
            class="spf-step-content-element-wrap flex w-1/12 py-[0.75rem] pl-[0.75rem] el-border-light gap-2"
          >
            <div class="spf-step-content-element-el-name flex w-full justify-center items-center">
              <CheckboxField
                v-model="service.is_preticked"
                class="mb-0 mr-1"
                :size="'20px'"
              ></CheckboxField>
            </div>
          </div>
          <div
            class="spf-step-content-element-wrap flex w-1/12 py-[0.75rem] pl-[0.75rem] el-border-light gap-2"
          >
            <div class="spf-step-content-element-el flex w-full justify-center items-center">
              <CheckboxField
                v-model="service.was_taken"
                class="mb-0 mr-1"
                :size="'20px'"
              ></CheckboxField>
            </div>
          </div>
          <div
            class="spf-step-content-element-wrap flex w-5/12 py-[0.75rem] px-[0.75rem] el-border-light gap-2"
          >
            <div class="spf-step-content-element-el flex w-full justify-center items-center">
              <InputField v-model="service.comments" class="mb-0 w-full" is-white />
            </div>
          </div>
        </div>
      </div>
      <div class="spf-step-pagination flex justify-between items-center w-full p-[0.75rem]">
        <div class="spf-step-pagination-perpage flex items-center w-full gap-2">
          <SelectField
            :searchable="false"
            :clearable="false"
            class="mb-0 max-w-[85px]"
            :options="[5, 10, 20]"
            :model-value="10"
          />
          <span class="w-full">entries per page</span>
        </div>
        <div class="spf-step-pagination-buttons flex">
          <div class="spf-step-pagination-button">Previous</div>
          <div class="spf-step-pagination-button active">1</div>
          <div class="spf-step-pagination-button">2</div>
          <div class="spf-step-pagination-button">3</div>
          <div class="spf-step-pagination-button">4</div>
          <div class="spf-step-pagination-button">5</div>
          <div class="spf-step-pagination-button">Next</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { type PropType, ref, watch } from 'vue';
import CheckboxField from '../forms/fields/CheckboxField.vue';
import InputField from '../forms/fields/InputField.vue';
import SelectField from '../forms/fields/SelectField.vue';
import Loading from '../forms/Loading.vue';

import type { IOrder } from 'shared/types';

const props = defineProps({
  isLoading: {
    type: Boolean as PropType<boolean>,
    default: false
  },
  order: {
    type: Object as PropType<IOrder>,
    default: null
  }
});

const mockServices = ref([
  {
    name: 'Handling Fee',
    is_preticked: true,
    was_taken: true,
    comments: 'Enim et pellentesque nec.'
  },
  {
    name: 'Passenger Handling',
    is_preticked: true,
    was_taken: true,
    comments: 'Enim et pellentesque nec.'
  },
  { name: 'Parking', is_preticked: true, was_taken: true, comments: 'Enim et pellentesque nec.' },
  { name: 'Parking', is_preticked: false, was_taken: false, comments: 'Enim et pellentesque nec.' },
  { name: 'Parking', is_preticked: false, was_taken: false, comments: 'Enim et pellentesque nec.' }
]);

watch(
  () => props.order,
  async (order: IOrder) => {
    if (order && order.type.is_gh) {
      // TO DO add backend
    }
  }
);
</script>

<style lang="scss">
.spf-step {
  .button {
    background-color: rgba(81, 93, 138, 1) !important;
    color: white !important;
    font-weight: 500 !important;
    font-size: 16px !important;
    @apply flex shrink-0 focus:shadow-none mb-0 mt-0 p-[0.5rem] px-[1rem] rounded-lg #{!important};

    &:disabled {
      background-color: rgb(190, 196, 217) !important;
      color: rgb(133, 141, 173) !important;
      border: transparent !important;
    }

    &.light-button {
      background-color: rgba(240, 242, 252, 1) !important;
      border: transparent !important;
      padding: 0.5rem !important;
    }
  }

  .download-button {
    background-color: rgba(240, 242, 252, 1);
    border-color: transparent;
    border-radius: 12px;
    box-shadow: none;
    padding: 10px;
  }

  .el-border {
    border-right: 1px solid rgb(223, 226, 236);

    &-light {
      border-right: 1px solid theme('colors.dark-background');
    }
  }

  &-header {
    color: theme('colors.main');
    font-size: 18px;
    font-weight: 600;
  }

  &-content {
    &-data-wrap {
      border-bottom: 1px solid theme('colors.dark-background');
      background-color: rgba(246, 248, 252, 0.5);

      &:last-of-type {
        border-radius: 0 0 8px 8px;
      }

      &.selected-supplier {
        background-color: rgba(255, 255, 255, 1) !important;

        .spf-step-content-col-data {
          color: rgba(39, 44, 63, 1);
          background-color: rgba(255, 255, 255, 1);
        }
      }
    }

    &-header-wrap {
      background-color: rgb(246, 248, 252);
    }

    &-header-big-wrap {
      background-color: rgba(246, 248, 252, 1);
    }

    &-header-big {
      &-el {
        background-color: rgba(223, 226, 236, 0.5);
        color: rgba(39, 44, 63, 1);
        font-size: 12px;
        font-weight: 500;
      }
    }

    &-header-sub {
      background-color: rgba(246, 248, 252, 1);

      &-el {
        color: rgba(82, 90, 122, 1);
        font-size: 11px;
        font-weight: 500;
      }
    }

    &-el {
      &-name {
        color: rgba(82, 90, 122, 1);
        font-size: 13px;
        font-weight: 500;
        min-width: 100px;
      }

      &-value {
        color: theme('colors.main');
        font-size: 14px;
        font-weight: 500;
      }
    }

    &-element {
      &-wrap {
        border-bottom: 1px solid rgba(246, 248, 252, 1);
      }

      &-el {
        color: rgba(39, 44, 63, 1);
        font-size: 13px;
        font-weight: 400;

        &-name {
          color: rgba(39, 44, 63, 1);
          font-size: 13px;
          font-weight: 500;
        }
      }
    }

    &-results {
      background-color: rgba(246, 248, 252, 1);

      &-el {
        &-name {
          color: rgba(82, 90, 122, 1);
          font-size: 11px;
          font-weight: 500;
          border-left: 1px solid rgb(223, 226, 236);
        }

        &-value {
          color: rgba(39, 44, 63, 1);
          font-size: 13px;
          font-weight: 600;
        }
      }
    }

    &-divider {
      text-transform: capitalize;
      background-color: rgba(246, 248, 252, 1);
      color: rgba(82, 90, 122, 1);
      font-size: 12px;
      font-weight: 500;
    }

    &-margin {
      &-name {
        color: rgba(39, 44, 63, 1);
        font-size: 13px;
        font-weight: 500;
      }

      &-value {
        color: rgba(11, 161, 125, 1);
        font-size: 16px;
        font-weight: 600;
      }
    }

    &-col {
      height: 100%;

      &-header {
        color: rgba(82, 90, 122, 1);
        font-size: 11px;
        font-weight: 500;
        background-color: rgb(246, 248, 252);
      }

      &-data {
        color: rgba(133, 141, 173, 1);
        font-size: 13px;
        font-weight: 400;

        .files-button {
          border: 1px solid rgba(223, 226, 236, 1);
          border-radius: 6px;
        }

        .horizontal {
          transform: rotate(90deg);
        }
      }
    }

    &-none {
      position: relative;
      background-color: rgba(255, 161, 0, 0.08);

      &-header {
        color: theme('colors.main');
        font-size: 14px;
        font-weight: 600;
      }

      &-desc {
        color: theme('colors.main');
        font-size: 12px;
        font-weight: 400;
      }
    }

    &-missing {
      background-color: rgba(246, 248, 252, 1);

      span {
        color: rgba(82, 90, 122, 1);
        font-size: 11px;
        font-weight: 500;
      }
    }
  }

  &-pagination {
    &-perpage {
      color: rgba(82, 90, 122, 1);
      font-size: 13px;
      font-weight: 500;
    }

    &-buttons {
      color: rgba(82, 90, 122, 1);
      font-size: 13px;
      font-weight: 500;
    }

    &-button {
      color: rgba(82, 90, 122, 1);
      font-size: 13px;
      font-weight: 500;
      cursor: pointer;
      padding: 0.375rem 0.75rem;
      border-top: 1px solid rgba(82, 90, 122, 1);
      border-bottom: 1px solid rgba(82, 90, 122, 1);
      border-right: 1px solid rgba(82, 90, 122, 1);

      &:first-of-type {
        border-radius: 0.5rem 0 0 0.5rem;
        border-left: 1px solid rgba(82, 90, 122, 1);
      }

      &:last-of-type {
        border-radius: 0 0.5rem 0.5rem 0;
      }

      &:hover {
        background-color: #e5e7eb;
        border-color: #d1d5db;
      }

      &.active {
        color: #fff;
        background-color: #515d8a;
      }
    }
  }
}
</style>
