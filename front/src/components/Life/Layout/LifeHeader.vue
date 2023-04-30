<template>
  <header class="header bg-gray-200 max-w-[1060px] mx-auto">
    <auth-dialog></auth-dialog>
    <div class="flex justify-between pr-3">
      <ul class="flex">
        <li 
          v-for="site in $store.foodSites" 
          class="h-12"
          :class="{'bg-[white] site-link-shadow': site.isActive}"
        >
          <a :href="site.link" target="_blank">
            <div class="flex flex-col items-center justify-center text-center px-5 pt-[9px] text-xs">
              <p>{{ site.name }}</p>
              <p class="whitespace-nowrap text-gray-500">{{ site.description }}</p>
            </div>
          </a>
        </li>
      </ul>
      <div class="flex items-center space-x-2 text-sm leading-6">
        <button class="flex items-center space-x-1 bg-yellow-400 rounded-full px-2.5">
          <img src="@/assets/food-icons/header/question.svg" width="16" height="16" />
          <span>
            Помощь
          </span>
        </button>
        <button class="flex items-center space-x-1 bg-gray-300 rounded-full px-2.5">
          <img src="@/assets/food-icons/header/phone.svg" width="16" height="16" />
          <span>
            +7 (771) 930-02-02
          </span>
        </button>
        <button class="flex items-center space-x-1 bg-gray-300 rounded-full px-2.5">Рус</button>
        <button class="flex items-center space-x-1 bg-gray-300 rounded-full px-2.5">Қаз</button>
      </div>
    </div>
    <div class="flex items-center px-5 bg-white h-[60px] justify-between mb-2">
      <button>
        <img src="@/assets/food-icons/header/logo.svg" width="136" height="33" />
      </button>
      <button class="flex items-center space-x-1">
        <img src="@/assets/food-icons/header/location.svg" width="16" height="12" />
        <span>Алматы</span>
      </button>
      <div class="border-[1px] border-gray-300 rounded-md h-10 flex items-center">
        <input placeholder="Я ищу..." class="pl-4" />
        <button class="px-2 bg-gray-200 text-gray-400 h-10">Найти</button>
      </div>
      <div v-if="!$store.hasLogged" class="space-x-4">
        <button 
          class="bg-yellow-300 h-10 w-24 rounded-lg"
          @click="$store.hasLogged ? null : $store.toggleFoodAuthModal()"
        >
          Войти
        </button>
        <button 
          class="text-blue-600"
          @click="$store.hasLogged ? null : $store.toggleFoodAuthModal()"
        >
          Создать аккаунт
        </button>
      </div>
      <div v-else class="space-x-4 flex flex-col items-center">
        <p>
          {{ $store.user.email }}
        </p>
        <button @click="$store.logout()">
          Выйти из аккаунта
        </button>
      </div>
      <div class="flex items-center space-x-2 relative border-l-[1px] border-l-gray-300 h-[30px] pl-2 hover:cursor-pointer">
        <img src="@/assets/food-icons/header/basket.svg" width="20" height="20" />
        <span class="text-sm">Корзина</span>
      </div>
    </div>
    <div>
      <ul class="flex items-center h-[50px] space-x-8 bg-white px-4">
        <li v-for="category in $store.categoriesList" :id="category.id">
          <button :class="{ 'text-red-400': category.isSelected }" @click="() => {
            $store.onCategoryClick(category.id);
            $router.replace('/chocolife');
          }">
            {{ category.title }}
          </button>
        </li>
      </ul>
    </div>
  </header>
</template>

<script>
  import { onMounted } from 'vue';
  import { useStore } from '@/store';
  export default {
    name: "LifeHeader",
    setup() {
      const store = useStore();
      console.log(store.hasLogged);
    
      onMounted(() => {
        store.getCategories();
      });
    }
  };

</script>

<style scoped>
  .site-link-shadow {
    box-shadow: 0 0 5px rgb(88 88 88 / 13%);
  }
</style>