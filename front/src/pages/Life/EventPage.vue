<template>
  <section class="max-w-[1060px] mx-auto pb-96">
    <div class="flex p-3 bg-white mt-8 space-x-3">
      <img :src="event.img" class="rounded-xl" />
      <div class="space-y-3">
        <p class="font-semibold text-xl">{{ event.title  }}</p>
        <p class="">{{ event.company.title }}</p>
        <div class="flex items-center space-x-2 py-1 max-w-[200px] px-2 rounded-xl bg-gray-200">
          <img src="@/assets/food-icons/header/location.svg" height="16" width="16" />
          <p class="truncate">{{ event.company.sale_points  }}</p>
        </div>
        <div class="flex items-center space-x-2 py-1 max-w-[350px] px-2 rounded-xl bg-gray-200">
          <img src="@/assets/food-icons/header/location.svg" height="16" width="16" />
          <p class="truncate text-sm">Можно купить до {{ format(new Date(event.use_until_date), 'd MMMM yyyy', { locale: ru }) }}</p>
        </div>
        <div class="flex items-center space-x-2 py-1 max-w-[350px] px-2 rounded-xl bg-gray-200">
          <img src="@/assets/food-icons/header/location.svg" height="16" width="16" />
          <p class="truncate text-sm">Использовать до {{ format(new Date(event.expiration_date), 'd MMMM yyyy', { locale: ru })  }}</p>
        </div>
      </div>
    </div>
    <div class="bg-white p-4 mt-4">
      <p class="text-sm font-semibold">ВИДЫ СЕРТИФИКАТОВ:</p>
      <ul class="flex flex-col space-y-4">
        <li v-for="cert in event.certificates" :key="cert.id">
          <div class="p-2 border-gray-200 border-[1px] rounded-sm space-y-3">
            <p>{{ cert.title }}</p>
            <div class="flex justify-between items-center">
              <p class="text-gray-400">Скидка {{ cert.discount }}%</p>
              <p class="text-gray-400">Купили {{ cert.bought_amount }} человек</p>
              <div>
                <p>{{ cert.initial_price -   cert.initial_price * cert.discount / 100 }} ₸</p>
                <p class="line-through text-gray-400">{{ cert.initial_price }} ₸</p>
              </div>
              <div class="space-x-2 mr-4">  
                <button class="bg-yellow-400 rounded-xl px-6 py-2 text-sm" @click="onBuyClick(cert, false)">Купить</button>
                <button class="bg-gray-200 px-6 py-2 text-sm rounded-xl" @click="onBuyClick(cert, true);">В корзину</button>
              </div>
            </div>
          </div>
        </li>
      </ul>
    </div>
  </section>
</template>

<script>
  import { useStore } from '@/store';
  import { format } from 'date-fns'
  import { ru } from 'date-fns/locale'
  import { useRouter } from 'vue-router';

  export default {
    props: {
      id: {
        type: String
      },
      event: {
        type: String
      }
    },
    setup(props) {
      const store = useStore();
      const router = useRouter();
      const event = JSON.parse(props.event);
  
      const onBuyClick = (cert, isPush) => {
        let isAdded = false;
        for (let i = 0; i < store.lifeBasket.length; ++i) {
          if (store.lifeBasket[i].id && event.cert && store.lifeBasket[i].id === event.id && event.cert.id === store.lifeBasket[i].cert.id) {
            store.lifeBasket[i].amount++;
            isAdded = true;
            break;
          }
        }
        if (!isAdded) {
          store.lifeBasket.push({ ...event, amount: 1, cert: { ...cert } });
        }
        if (!isPush) {
          router.replace({ name: 'chocolifePayment' });
        }
      }

      return {
        event,
        format,
        ru,
        onBuyClick
      }
    }
  }
</script>