<template>
  <div id="userData">
  <b-card title="User Data"
          tag="article"
          class="mb-2 user-card">
    <ul class="list-group">
      <li v-for="(data, index) in datas" v-bind:key="index" class="list-group-item">{{data['UserId']['S']}}</li>
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
      datas: ["test1", "test2", "test3"],
      error: ""
    }
  },
  methods: {
      
  },

  created() {
    console.log("TEST");
        var params = {
            TableName : "ShoppinParse"
        };
        database.scan(params, (err, data) => {
            //console.log(err);
            if (err) {
                this.error = "Unable to query. Error: " + "\n" + JSON.stringify(err, undefined, 2);
            } else {
                //console.log(JSON.stringify(data['Items']));
                this.datas = data['Items'];
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
.user-card {
  margin: 0 auto;
  margin-top: 10px;
  padding: 10px;
}
</style>