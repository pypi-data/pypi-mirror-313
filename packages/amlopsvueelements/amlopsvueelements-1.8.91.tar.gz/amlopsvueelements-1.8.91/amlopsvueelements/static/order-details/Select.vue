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
      { 'ops-form-select__no_indicator': !hasIndicator },
      { 'ops-form-select__white': isWhite },
      { 'ops-form-select__half': isHalf }
    ]"
    @search="handleSearch"
  >
    <template #open-indicator="slotProps">
      <div :class="[$style['ops-form-select__arrow-wrapper']]">
        <b v-bind="slotProps.attributes" :class="[$style['ops-form-select__arrow']]" />
      </div>
    </template>
    <template #option="item">
      <slot name="select-option" v-bind="{ item }" />
    </template>
    <template v-for="(_, name) in $slots" #[name]="slotData">
      <slot :name="name" v-bind="{ slotData }" />
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
  },
  isWhite: {
    type: Boolean,
    default: false
  },
  isHalf: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits<{
  (e: 'search', value: string): void;
}>();

const handleSearch = (value: string) => {
  emit('search', value); // Emit 'search' event with the value to parent
};
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
.ops-form-select__no_indicator {
  border-radius: 0.5rem;
}

.ops-form-select__indicator {
  border-radius: 0.5rem 0 0 0.5rem !important;
}

.ops-form-select__white {
  background: #fff !important;
  border: 1px solid rgb(223, 226, 236) !important;

  .vs__dropdown-toggle {
    border-color: transparent !important;
    min-height: 2.5rem !important;
    box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.07);
  }

  .vs__selected-options {
    padding-left: 10px !important;
    padding-right: 0 !important;
  }

  .vs__clear {
    display: none !important;
  }
}

.ops-form-select__half {
  border-radius: 0 0.5rem 0.5rem 0 !important;
  border-left: none !important;
  .vs__search {
    display: none !important;
  }

  .vs__dropdown-toggle {
    border-radius: 0 0.5rem 0.5rem 0 !important;
  }

  &.vs--disabled {
    cursor: auto !important;
    background: #fff !important;
    border-radius: 0 0.5rem 0.5rem 0 !important;
    .vs__dropdown-toggle {
      background: #fff !important;
      border-radius: 0 0.5rem 0.5rem 0 !important;
      box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.07);
      cursor: auto !important;

      .vs__search {
        cursor: auto !important;
      }

      .vs__selected {
        cursor: auto !important;
      }
      .vs__actions {
        display: none;
      }
    }
  }
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

  &__search {
    @apply m-0 #{!important};
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
        @apply flex items-center p-1 gap-1 #{!important};

        input {
          &::placeholder {
            @apply pl-2 #{!important};
          }
        }
      }

      @apply block rounded-[0.5rem] cursor-pointer truncate max-w-[90%] border-transparent duration-500 font-bold text-white text-[0.875rem] bg-grey-900 py-[0.2rem] px-[0.5rem] #{!important};

      background-color: rgb(255, 255, 255) !important;
      color: rgba(21, 28, 53, 1) !important;
      font-size: 16px !important;
      font-weight: 400 !important;

      &:hover {
        @apply border-transparent #{!important};
        background-color: rgb(81, 93, 138) #{!important};
        color: rgb(255, 255, 255) !important;

        & > button > svg {
          @apply fill-white #{!important};
        }
      }

      & > button > svg {
        @apply fill-[#8b94b2] #{!important};
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
