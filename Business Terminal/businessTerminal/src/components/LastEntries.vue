<template>
  <div id="lastEntries">
  <b-card title="Last purchases"
          tag="article"
          class="mb-2 entries-card">
    <ul class="list-group">
      <li v-for="(purchase, index) in purchases" v-bind:key="index" class="list-group-item">
        <h5>{{ purchase['Position']['S'] }} - {{ purchase['DateTime']['S'] }} - {{ centToEuro(purchase['TotalPrice']['N']) }} €</h5>       
        <ul>
          <li v-for="(item, index2) in resolveObjects(purchase['Items']['M'])" v-bind:key="index2">
            <p>{{ item }}</p>
          </li>
        </ul>
        
      </li>
    </ul>
    
    <p>{{error}}</p>
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
      purchases: []
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
      }
  },

  created() {
    console.log("TEST");
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
                
            }
        });
  }

  /*
  created() {
    console.log("TEST");
        var params = {
            TableName : "Shopping",
            KeyConditionExpression: "#userid = :id",
            ExpressionAttributeNames:{
                "#userid": "UserId"
            },
            ExpressionAttributeValues: {
                ":id": {"S":"12345"}
            }
        };
        database.scan(params, (err, data) => {
            console.log(err);
            if (err) {
                this.error = "Unable to query. Error: " + "\n" + JSON.stringify(err, undefined, 2);
            } else {
                console.log(data)
                this.datas = data['Items'];
            }
        });
  }
  */
}
</script>

<style>
.entries-card {
  margin: 0 auto;
  margin-top: 10px;
  padding: 10px;
}
</style>