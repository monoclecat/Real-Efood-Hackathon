<template>
  <div id="selectUser">
  <b-card title="Data per User"
          tag="article"
          class="mb-2 user-card">
    <b-form-select v-model="selected" :options="options" class="mb-3">
    </b-form-select>
    <div>Selected: <strong>{{ selected }}</strong></div>
    <button v-on:click="selectedDid">Search</button>
    <p>{{error}}</p>


    <ul class="list-group">
      <li v-for="(selPurch, index) in selectPurchases" v-bind:key="index">
        <ul>
          <li v-for="(item, index2) in selPurch" v-bind:key="index2">
            {{ item }}
        </li>
        </ul>
      </li>
    </ul>

  </b-card>
  </div>
</template>

<script>
import { database } from '../aws.config.js';
export default {
  data () {
    return {
      datas: [],
      error: "",
      users: [],
      purchasesByUser: [],
      purchases: [],
      selected: null,
      options: [],
      selectPurchases: []
    }
  },
  methods: {
    centToEuro: function(price) {
      return price / 100;
    },
    resolveObjects: function(object) {
      let products = [];
      for (let product in object) {
        products.push(object[product]['M']['Amount']['N'] + " mal - " + product + " für - " + this.centToEuro(object[product]['M']['Price']['N']) + " €");
      }
      return products;
    },
    selectedDid: function(event) {
      this.selectPurchases = [];
      for (let i = 0; i < this.datas.length; i++) {
      if (this.datas[i]['UserId']['S'] == this.selected) {
        for (let j = 0; j < this.datas[i]['Purchases']['L'].length; j++) {
          //this.selectPurchases.push(this.datas[i]['Purchases']['L'][j]['M']['Items']);
          console.log(JSON.stringify(this.datas[i]['Purchases']['L'][j]['M']['Items']['M']));
          this.selectPurchases.push(this.resolveObjects(this.datas[i]['Purchases']['L'][j]['M']['Items']['M']));
        }
      }
    }
    }
  },
  created() {
        var params = {
            TableName : "ShoppinParse"
        };
        database.scan(params, (err, data) => {
            console.log(err);
            if (err) {
                this.error = "Unable to query. Error: " + "\n" + JSON.stringify(err, undefined, 2);
            } else {
                this.datas = data['Items'];

                for (var i = 0; i < this.datas.length; i++) {
                  this.users.push(this.datas[i]['UserId']['S']);
                }

                for (var i = 0; i < this.datas.length; i++) {
                  this.purchasesByUser.push(this.datas[i]['Purchases']['L']);
                }
                
                for (var i = 0; i < this.purchasesByUser.length; i++) {
                  for (var j = 0; j < this.purchasesByUser[i].length; j++) {
                    this.purchases.push(this.purchasesByUser[i][j]['M']);
                  }
                }

                // Build select options
                for (var i = 0; i < this.datas.length; i++) {
                  this.options.push({value: this.users[i], text: this.users[i]});
                }
            }
        });
  },
  updated() {
    
  }
}
</script>

<style>

</style>