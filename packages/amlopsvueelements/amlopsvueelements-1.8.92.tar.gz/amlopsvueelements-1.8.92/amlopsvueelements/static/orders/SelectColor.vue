<template>
  <VueSelect
    v-bind="$attrs"
    :append-to-body="appendToBody"
    :class="[
      $style['ops-form-select'],
      { 'ops-form-select__error': hasErrors },
      { 'ops-form-select__position-top': position === 'top' },
      { 'ops-form-select__hide-values': hideValues },
      { 'ops-form-select__indicator': hasIndicator },
      { 'ops-form-select__no_indicator': !hasIndicator }
    ]"
  >
    <template #open-indicator="slotProps">
      <div :class="[$style['ops-form-select__arrow-wrapper']]">
        <b v-bind="slotProps.attributes" :class="[$style['ops-form-select__arrow']]" />
      </div>
    </template>
    <template #selected-option="item">
      <div class="select-option">
        <div class="square" :style="{ 'background-color': item.fill_colour_hex }"></div>
        {{ item.name }}
      </div>
    </template>
    <template #option="item">
      <div class="select-option">
        <div class="square" :style="{ 'background-color': item.fill_colour_hex }"></div>
        {{ item.name }}
      </div>
    </template>
  </VueSelect>
</template>

<script lang="ts" setup>
// @ts-ignore
import VueSelect from 'vue-select';
import 'vue-select/dist/vue-select.css';

defineProps({
  hasErrors: {
    type: Boolean,
    default: false
  },
  hideValues: {
    type: Boolean,
    default: false
  },
  position: {
    type: String,
    default: ''
  },
  appendToBody: {
    type: Boolean,
    default: true
  },
  hasIndicator: {
    type: Boolean,
    default: false
  }
});
</script>
<style lang="scss" module scoped>
.ops-form-select {
  background: #eff1f6;

  &__arrow-wrapper {
    @apply absolute cursor-pointer h-full;
  }

  &__arrow {
    @apply border-solid mt-[-2px] cursor-pointer ml-[-4px] absolute w-0 top-1/2 left-1/2 h-0;
    border-color: #888 transparent transparent transparent;
    border-width: 5px 4px 0 4px;
  }

  &__indicator {
    border-radius: 0.5rem 0 0 0.5rem !important;
  }

  @apply w-full cursor-pointer;
}
</style>
<style lang="scss">
.select-option {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  width: 100%;
  justify-content: flex-start;
}

.square {
  height: 10px;
  min-width: 10px;
}

.ops-form-select__no_indicator {
  border-radius: 0.5rem;
}

.ops-form-select__indicator {
  border-radius: 0.5rem 0 0 0.5rem !important;
}

.vs {
  &--single {
    &:is(.vs--open) {
      .vs__selected {
        opacity: 0 !important;
      }
    }
  }

  &--disabled {
    @apply rounded-full cursor-not-allowed #{!important};
  }

  &__dropdown {
    &-toggle {
      border: 1px solid #eff1f6 !important;
      @apply text-[0.875rem] h-fit leading-6 text-grey-700 w-full min-h-[2.625rem] p-0 #{!important};
    }

    &-menu {
      @apply rounded-[0.5rem] max-h-[15rem] border-transparent py-0 mt-2 border-solid text-base text-grey-900 font-normal #{!important};
    }

    &-option {
      @apply bg-white font-normal pl-4 text-[1rem] hover:text-grey-900 overflow-hidden truncate p-[6px] leading-6 font-normal #{!important};

      &:hover {
        background-color: rgba(125, 148, 231, 0.1) !important;
        color: rgb(125, 148, 231) !important;
      }

      &--highlight {
        background-color: rgba(125, 148, 231, 0.1) !important;
        color: rgb(125, 148, 231) !important;
      }
    }
  }

  &__deselect {
    @apply ml-2 #{!important};
  }

  &__selected {
    @apply pl-0 ml-0 mt-[1px] #{!important};

    &-options {
      @apply flex items-center py-0 px-[0.625rem] pl-[17px] w-[70%] lg:w-[90%] #{!important};

      input {
        &::placeholder {
          @apply text-base text-grey-200 font-light #{!important};
        }
      }
    }

    @apply block truncate max-w-[90%] font-medium text-grey-950 text-[0.875rem] #{!important};
  }

  &__spinner {
    @apply absolute rounded-[50%] right-[0.5rem] #{!important};
  }

  &__actions {
    @apply pr-[1rem] pt-0 pl-0 pb-0 #{!important};
  }

  &__clear {
    @apply absolute cursor-pointer z-50 leading-[2.5rem] top-[1.0625rem] text-[#888] mr-0 font-bold right-[2.25rem] #{!important};
  }
}

.v-select.mb-0 {
  .vs__clear {
    top: auto !important;
  }
}

.v-select.ops-form-select__position-top:has(.vs__dropdown-menu) {
  .vs__dropdown-toggle {
    @apply rounded-t-none rounded-b-[0.5rem] h-fit duration-500 #{!important};
  }
}

.v-select {
  &:is(.ops-form-select__position-top) {
    .vs__dropdown-menu {
      @apply top-auto rounded-t-[0.5rem] bottom-[calc(100%-1px)] shadow-none rounded-b-none #{!important};
    }
  }

  &:is(.ops-form-select__hide-values) {
    .vs__dropdown-toggle > .vs__selected-options > .vs__selected {
      display: none !important;
    }
  }

  &:has(.vs__dropdown-menu) {
    .vs__dropdown-toggle {
      @apply rounded-b-none h-fit duration-500 #{!important};
    }
  }

  &:is(.vs--multiple) {
    .vs__selected {
      &-options {
        @apply flex items-center #{!important};
      }

      @apply block rounded-[0.5rem] cursor-pointer truncate max-w-[90%] border-grey-900 duration-500 font-bold text-white text-[0.875rem] bg-grey-900 py-[0.2rem] px-[0.5rem] #{!important};

      &:hover {
        @apply bg-confetti-500 border-transparent text-grey-900 #{!important};

        & > button > svg {
          @apply fill-grey-500 #{!important};
        }
      }

      & > button > svg {
        @apply fill-white #{!important};
      }
    }
  }
}

.ops-form-select__error {
  .vs__dropdown-toggle {
    @apply border-amaranth-900 #{!important};
  }
}
</style>
