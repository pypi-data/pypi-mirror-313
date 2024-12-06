<template>
  <div class="order-step bg-white w-full border border-transparent rounded-md">
    <div class="order-step-header flex justify-between items-center py-[0.75rem] px-[0.75rem]">
      <div class="order-step-header-name">Client Documents</div>
    </div>
    <div
      v-if="documents?.length === 0"
      class="order-step-content-missing flex items-center justify-center py-[1.25rem]"
    >
      <Loading v-if="isLoadingDocuments" />
      <span>There are no client documents to display</span>
    </div>
    <div v-else class="order-step-content w-full flex flex-col">
      <div class="order-step-content-header-wrap w-full flex items-center">
        <div class="order-step-content-col w-3/12">
          <div class="order-step-content-col-header px-[0.75rem] py-[0.5rem]">Type</div>
        </div>
        <div class="order-step-content-col w-2/12">
          <div class="order-step-content-col-header px-[0.75rem] py-[0.5rem]">Name</div>
        </div>
        <div class="order-step-content-col w-2/12">
          <div class="order-step-content-col-header px-[0.75rem] py-[0.5rem]">Entity</div>
        </div>
        <div class="order-step-content-col w-2/12">
          <div class="order-step-content-col-header px-[0.75rem] py-[0.5rem]">Valid From</div>
        </div>
        <div class="order-step-content-col w-2/12">
          <div class="order-step-content-col-header px-[0.75rem] py-[0.5rem]">Valid To</div>
        </div>
        <div class="order-step-content-col w-1/12">
          <div class="order-step-content-col-header px-[0.75rem] py-[0.5rem]">&nbsp;</div>
        </div>
      </div>
      <div
        v-for="(document, index) in documents"
        :key="index"
        class="order-step-content-data-wrap selected-supplier w-full flex items-center"
      >
        <div class="order-step-content-col w-3/12">
          <div class="order-step-content-col-data px-[0.75rem] py-[0.5rem]">
            {{ document.document_type }}
          </div>
        </div>
        <div class="order-step-content-col w-2/12">
          <div class="order-step-content-col-data px-[0.75rem] py-[0.5rem]">
            {{ document.document_name }}
          </div>
        </div>
        <div class="order-step-content-col w-2/12">
          <div class="order-step-content-col-data px-[0.75rem] py-[0.5rem]">
            {{ document.entity_name }}
          </div>
        </div>
        <div class="order-step-content-col w-2/12">
          <div class="order-step-content-col-data px-[0.75rem] py-[0.5rem]">
            {{ document.valid_from_date }}
          </div>
        </div>
        <div class="order-step-content-col w-2/12">
          <div class="order-step-content-col-data px-[0.75rem] py-[0.5rem]">
            {{ document.valid_to_date }}
          </div>
        </div>
        <div class="order-step-content-col w-1/12">
          <div class="order-step-content-col-data px-[0.75rem] py-[0.5rem]">
            <a
              v-if="document.download_url"
              :title="getFilenameByUrl(document.download_url)"
              :href="document.download_url"
              :download="getFilenameByUrl(document.download_url)"
            >
              <Button class="download-button">
                <img
                  width="20"
                  height="20"
                  src="../../assets/icons/download.svg"
                  alt="options"
                  class="horizontal cursor-pointer" /></Button
            ></a>
            <span v-else class="pl-[14px]">--</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue';
import { Button } from 'shared/components';
import { useOrderStore } from '@/stores/useOrderStore';
import { useQueryOrderClientDocuments } from '@/services/queries';
import { getFilenameByUrl } from '@/helpers/files';
import Loading from '../forms/Loading.vue';

const orderStore = useOrderStore();
const orderId = computed(() => orderStore.order?.id);
const enabled = ref(false);

const { data: documents, isPending: isLoadingDocuments } = useQueryOrderClientDocuments(orderId, {
  enabled
});

watch(
  () => [orderStore.order?.id, orderStore.currentStep, orderStore.order?.type?.is_fuel],
  ([id, step, isFuel]) => {
    enabled.value = !!(id && ((step === 3 && isFuel) || (step === 2 && !isFuel)));
  }
);
</script>

<style lang="scss">
.credit {
  &-wrap {
    padding-top: 28px;
    background: rgb(245, 246, 249);
    border-radius: 4px 4px 0 0;
  }

  &-missing {
    background-color: rgba(246, 248, 252, 1);

    span {
      color: rgba(82, 90, 122, 1);
      font-size: 11px;
      font-weight: 500;
    }
  }

  &-confirmed {
    background-color: rgb(255, 255, 255);

    &-value {
      border-left: 4px solid rgba(98, 132, 254, 1);
      color: theme('colors.main');
      font-size: 18px;
      font-weight: 600;

      &-name {
        color: rgba(82, 90, 122, 1);
        font-size: 12px;
        font-weight: 400;
      }
    }

    &-graph {
      height: 40px;
      width: 100%;
      background-color: rgba(98, 132, 254, 1);
      border-radius: 4px 0 0 4px;
    }
  }

  &-open {
    background-color: rgb(255, 255, 255);

    &-value {
      border-left: 4px solid rgba(243, 173, 43, 1);
      color: theme('colors.main');
      font-size: 18px;
      font-weight: 600;

      &-name {
        color: rgba(82, 90, 122, 1);
        font-size: 12px;
        font-weight: 400;
      }
    }

    &-graph {
      height: 40px;
      width: 100%;
      background-color: rgba(243, 173, 43, 1);
    }
  }

  &-maximum {
    background-color: rgb(255, 255, 255);
    position: relative;

    &-value {
      border-left: 4px dashed rgba(254, 98, 98, 1);
      color: theme('colors.main');
      font-size: 18px;
      font-weight: 600;

      &-name {
        color: rgba(82, 90, 122, 1);
        font-size: 12px;
        font-weight: 400;
      }
    }

    &-graph {
      height: 40px;
      width: 100%;
      background: repeating-linear-gradient(
        120deg,
        rgba(254, 98, 98, 1),
        rgba(254, 98, 98, 1) 1px,
        rgb(223, 243, 231) 0,
        rgb(223, 243, 231) 12px
      );
    }

    &.no-overuse {
      .credit-maximum-value {
        border-left: 4px dashed rgba(243, 173, 43, 1);
      }

      .credit-maximum-graph {
        background: repeating-linear-gradient(
          120deg,
          rgba(243, 173, 43, 1),
          rgba(243, 173, 43, 1) 1px,
          rgb(223, 243, 231) 0,
          rgb(223, 243, 231) 12px
        );
      }
    }

    &-popup {
      width: max-content;
      position: absolute;
      right: 0;
      top: -14px;
      color: rgba(39, 44, 63, 1);
      font-size: 12px;
      font-weight: 400;
      background: rgba(255, 255, 255, 1);
      border: 1px solid rgba(139, 148, 178, 1);
      border-radius: 4px 4px 0px 4px;

      span {
        font-size: 14px;
        font-weight: 600;
      }

      &-line {
        position: absolute;
        width: 1px;
        right: -1px;
        height: 100%;
        background-color: rgba(139, 148, 178, 1);
      }

      &-dot {
        position: absolute;
        z-index: 1;
        width: 5px;
        right: -3px;
        height: 5px;
        top: 50px;
        border-radius: 50%;
        background-color: rgba(139, 148, 178, 1);
      }
    }
  }

  &-remaining {
    position: relative;
    background-color: rgb(255, 255, 255);

    &-value {
      border-left: 4px solid rgb(223, 243, 231);
      color: theme('colors.main');
      font-size: 18px;
      font-weight: 600;

      &-name {
        color: rgba(82, 90, 122, 1);
        font-size: 12px;
        font-weight: 400;
      }
    }

    &-graph {
      height: 40px;
      width: calc(100% + 1px);
      background-color: rgb(223, 243, 231);
    }

    &-popup {
      position: absolute;
      width: max-content;
      right: -1px;
      top: -48px;
      color: rgba(39, 44, 63, 1);
      font-size: 12px;
      font-weight: 400;
      background: rgba(255, 255, 255, 1);
      border: 1px solid rgba(139, 148, 178, 1);
      border-radius: 4px 4px 0px 4px;

      span {
        font-size: 14px;
        font-weight: 600;
      }

      &-line {
        position: absolute;
        width: 1px;
        top: 28px;
        right: -1px;
        height: 59px;
        background-color: rgba(139, 148, 178, 1);
      }

      &-dot {
        position: absolute;
        width: 5px;
        right: -3px;
        height: 5px;
        top: 84px;
        border-radius: 50%;
        background-color: rgba(139, 148, 178, 1);
      }
    }
  }

  &-overuse {
    position: relative;
    background-color: rgb(255, 255, 255);

    &-value {
      border-left: 4px solid rgba(254, 98, 98, 0.12);
      color: rgba(254, 98, 98, 1);
      font-size: 18px;
      font-weight: 600;

      &-name {
        color: rgba(82, 90, 122, 1);
        font-size: 12px;
        font-weight: 400;
      }
    }

    &-graph {
      height: 40px;
      width: calc(100% + 1px);
      background: repeating-linear-gradient(
        120deg,
        rgba(254, 98, 98, 1),
        rgba(254, 98, 98, 1) 1px,
        rgb(254, 236, 236) 0,
        rgb(254, 236, 236) 12px
      );
      background-color: rgba(254, 98, 98, 0.12);
      border-radius: 0 4px 4px 0;
    }

    &-popup {
      position: absolute;
      width: max-content;
      right: -1px;
      top: -48px;
      color: rgba(39, 44, 63, 1);
      font-size: 12px;
      font-weight: 400;
      background: rgba(255, 255, 255, 1);
      border: 1px solid rgba(139, 148, 178, 1);
      border-radius: 4px 4px 0px 4px;

      span {
        font-size: 14px;
        font-weight: 600;
        color: rgba(254, 98, 98, 1);
      }

      &-line {
        position: absolute;
        width: 1px;
        top: 28px;
        right: -1px;
        height: 59px;
        background-color: rgba(139, 148, 178, 1);
      }

      &-dot {
        position: absolute;
        width: 5px;
        right: -3px;
        height: 5px;
        top: 84px;
        border-radius: 50%;
        background-color: rgba(139, 148, 178, 1);
      }
    }
  }

  &-message {
    border: 1px solid rgba(139, 148, 178, 1);
    border-radius: 4px;
    color: rgba(39, 44, 63, 1);
    font-size: 15px;
    font-weight: 400;
  }
}
</style>
