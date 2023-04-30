<template>
  <button
    class="food-btn food-btn-green food-btn-green-rounded shadow"
    :class="`${size}`"
  >
    {{ text }}
  </button>
</template>

<script>
export default {
  name: "FoodGreenButton",
  props: {
    text: {
      type: String,
      default: "Кнопка",
    },
    size: {
      type: String,
      default: "lg",
    },
  },
};
</script>
