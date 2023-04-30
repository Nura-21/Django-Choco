import axios from "@/plugins/axios";

const methods = {
  POST: "POST",
  GET: "GET",
  DELETE: "DELETE",
  PUT: "PUT",
};

class ApiClass {
  async axiosCall(config) {
    const { data } = await axios.request(config);
    return data;
  }

  async login(userCredentials) {
    return await this.axiosCall({
      method: methods.POST,
      url: "/users/login",
      data: userCredentials,
    });
  }

  async addUser(userData) {
    return await this.axiosCall({
      method: methods.POST,
      url: "/users/",
      data: userData,
    });
  }

  async getUser(id) {
    return await this.axiosCall({
      method: methods.GET,
      url: `/users/${id}`,
    });
  }

  async updateProfile(data) {
    return await this.axiosCall({
      method: methods.PUT,
      url: `/users`,
      data: data,
    });
  }

  async getUsers() {
    return await this.axiosCall({
      method: methods.GET,
      url: "/users",
    });
  }

  async getFoodCategories() {
    return await this.axiosCall({
      method: methods.GET,
      url: "/food/restaurant-categories",
    });
  }

  async getFoodRestaurantByCategory(id) {
    return await this.axiosCall({
      method: methods.GET,
      url: `/food/restaurants/?category_id=${id}`,
    });
  }

  async searchRestaurants(query) {
    return await this.axiosCall({
      method: methods.GET,
      url: `/food/restaurants/?search=${query}`,
    });
  }

  async getFoodRestaurant() {
    return await this.axiosCall({
      method: methods.GET,
      url: `/food/restaurants/`,
    });
  }

  async getFoodRest(id) {
    return await this.axiosCall({
      method: methods.GET,
      url: `/food/restaurants/${id}`,
    });
  }

  async getFoodRestProducts(id) {
    return await this.axiosCall({
      method: methods.GET,
      url: `/food/restaurants/${id}/products/`,
    });
  }

  async getFoodRestCategories(id) {
    return await this.axiosCall({
      method: methods.GET,
      url: `/food/restaurants/${id}/product_categories/`,
    });
  }

  async makeOrder(data) {
    return await this.axiosCall({
      method: methods.POST,
      url: "/food/orders/",
      data: data,
    });
  }

  async payOrder(orderId, data) {
    return await this.axiosCall({
      method: methods.PUT,
      url: `/food/orders/${orderId}/pay/`,
      data: data,
    });
  }

  async cancelOrder(orderId, data) {
    return await this.axiosCall({
      method: methods.PUT,
      url: `/food/orders/${orderId}/cancel/`,
      data: data,
    });
  }

  async getFoodOrders() {
    return await this.axiosCall({
      method: methods.GET,
      url: `/food/orders`,
    });
  }

  async getUserCreditCards() {
    return await this.axiosCall({
      method: methods.GET,
      url: `/users/creditCards`,
    });
  }
  
  async getEvents() {
    return this.axiosCall({
      method: methods.GET,
      url: "/life/events"
    });
  }

  async addUserCard(data) {
    return await this.axiosCall({
      method: methods.POST,
      url: `/users/creditCards`,
      data: data,
    });
  }

  async deleteUserCard(cardId) {
    return await this.axiosCall({
      method: methods.DELETE,
      url: `/users/creditCards/${cardId}?`,
    });
  }

  async getReviews(restId) {
    return await this.axiosCall({
      method: methods.GET,
      url: `/food/reviews/?${restId}`,
    });
  }

  async makeReview(data) {
    return await this.axiosCall({
      method: methods.POST,
      url: "/food/reviews/",
      data: data,
    });
  }

  async getCategories() {
    return this.axiosCall({
      method: methods.GET,
      url: "life/event-categories"
    })
  }

  async getCategoryEvents(data) {
    return this.axiosCall({
      method: methods.GET,
      url: `life/events`,
      params: data
    })
  }

  async getLifeCompanies() {
    return this.axiosCall({
      method: methods.GET,
      url: 'life/companies'
    })
  }

  async getLifeCertificates() {
    return this.axiosCall({
      method: methods.GET,
      url: 'life/certificates'
    })
  }
}

export const api = new ApiClass();
