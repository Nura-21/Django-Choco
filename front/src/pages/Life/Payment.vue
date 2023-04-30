<template>
  <section class="max-w-[1060px] mx-auto pb-96 space-y-6">
    <h3>ПОКУПКА ДИСКОНТА</h3>
    <div class="flex space-x-6">
      <div class="bg-white space-y-6 py-2 px-4 max-w-[65%]">
        <p class="font-black">ВАШ ЗАКАЗ</p>
        <div v-for="event in $store.lifeBasket" class="flex justify-between items-center">
          <div class="max-w-[33%]">
            <p class="font-black" >{{ event.title }}</p>
            <p>{{ event.cert.title }}</p>
          </div>
          <p>{{ event.cert.initial_price - event.cert.initial_price * event.cert.discount / 100 }} ₸</p>
          <div class="flex items-center space-x-3">
            <button class="flex justify-center items-center w-3 h-3 p-3 rounded-full bg-yellow-300" @click="event.amount !== 1 ? event.amount-- : null">-</button>
            <p>{{ event.amount }}</p>
            <button class="flex justify-center items-center w-3 h-3 p-3 rounded-full bg-yellow-300" @click="event.amount++">+</button>
          </div>
          <div>
            <p></p>
            <button @click="removeItem(event)">Удалить</button>
          </div>
        </div>
      </div>
      <div class="flex flex-col justify-start items-start space-y-4 min-w-[30%] bg-white h-fit p-4">
        <p class="font-black">СПИСАНИЕ СРЕДСТВ</p>
        <p class="flex justify-between w-full">
          <span>С банковской карты</span> 
          <span>{{ getTotalPrice }} ₸</span>
        </p>
        <p class="flex justify-between w-full">
          <span>Сумма к оплате</span> 
          <span>{{ getTotalPrice }} ₸</span>
        </p>
        <button class="py-2 px-6 w-full text-center bg-yellow-400 rounded-xl">Оплатить</button>
      </div>
    </div>
  </section>
</template>

<script>
import { useStore } from '@/store';
import { computed } from 'vue';


  export default {
    setup() {
      const store = useStore();

      const removeItem = (event) => {
        for (let i = 0; i < store.lifeBasket.length; ++i) {
          if (store.lifeBasket[i].id === event.id && event.cert.id === store.lifeBasket[i].cert.id) {
            store.lifeBasket = [...store.lifeBasket.slice(0, i), ...store.lifeBasket.slice(i + 1, store.lifeBasket.length)];
            break;
          }
        }
      }

      const getTotalPrice = computed(() => {
        let total = 0; 
        store.lifeBasket.forEach(item => {
          total += item.cert.initial_price - item.cert.initial_price * item.cert.discount / 100
        })
        return total;
      })

      return {
        removeItem,
        getTotalPrice
      }
    }
  }

</script>