<template>
  <div
    uk-height-viewport="offset-bottom: 80px"
    class="uk-flex  uk-flex-middle uk-flex-column"
  >
    <h1>App Developer Form</h1>
     <FormulateInput
  type="file"
  name="file"
  label="Select zip file to upload"
  help="Select a zip file to upload"
/> 
<button>Deploy</button>

<table class="uk-table">
    <thead>
        <tr>
        <th></th>
            <th>Model Name</th>
            <th>End Point</th>
            <th>Request Type</th>
            <th>Response Type</th>
            
        </tr>
    </thead>
    <tbody>
        <tr v-for="(item,index) in models" :key="item.model_name">
        <td>
        <FormulateInput
  v-model="models[index]['value']"
  type="checkbox"
/>
</td>
            <td>{{item.model_name}}</td>
            <td>{{item.endpoint}}</td>
             <td><modal :name="`model-${item.model_name}-req`">
        <code>{{item.request_type}}</code>
    </modal>
    <button @click="clicked(`model-${item.model_name}-req`)">Request Format</button></td>
    <td><modal :name="`model-${item.model_name}-res`">
        <code>{{item.response_type}}</code>
    </modal>
    <button @click="clicked(`model-${item.model_name}-res`)">Response Format</button></td>
            
        </tr>
        
    </tbody>
    </table>


    <table class="uk-table">
    <thead>
        <tr>
        <th></th>
            <th>Sensor Name</th>
            <th>End Point</th>
            <th>Request Type</th>
            <th>Response Type</th>
            
        </tr>
    </thead>
    <tbody>
        <tr v-for="(item,index) in sensors" :key="item.sensor_name">
        <td>
        <FormulateInput
  v-model="sensors[index]['value']"
  type="checkbox"
/>
</td>
            <td>{{item.sensor_name}}</td>
            <td>{{item.endpoint}}</td>
            <td><modal :name="`sensor-${item.sensor_name}-req`">
        <code>{{item.request_type}}</code>
    </modal>
    <button @click="clicked(`sensor-${item.sensor_name}-req`)">Request Format</button></td>
    <td><modal :name="`sensor-${item.sensor_name}-res`">
        <code>{{item.response_type}}</code>
    </modal>
    <button @click="clicked(`sensor-${item.sensor_name}-res`)">Response Format</button></td>
       
        </tr>
        
    </tbody>
    </table>


        <table class="uk-table">
    <thead>
        <tr>
        <th></th>
            <th>Controller Name</th>
            <th>End Point</th>
            <th>Request Type</th>
            <th>Response Type</th>
            
        </tr>
    </thead>
    <tbody>
        <tr v-for="(item,index) in controllers" :key="item.controller_name">
        <td>
        <FormulateInput
  v-model="controllers[index]['value']"
  type="checkbox"
/>
</td>
            <td>{{item.controller_name}}</td>
            <td>{{item.endpoint}}</td>
             <td><modal :name="`controller-${item.controller_name}-req`">
        <code>{{item.request_type}}</code>
    </modal>
    <button @click="clicked(`controller-${item.controller_name}-req`)">Resquest Format</button></td>
    <td><modal :name="`controller-${item.controller_name}-res`">
        <code>{{item.response_type}}</code>
    </modal>
    <button @click="clicked(`controller-${item.controller_name}-res`)">Response Format</button></td>
        </tr>
        
    </tbody>
    </table>
    <pre
      class="code"
      v-text="models"
    />
  </div>

</template>

<script>
import { AUTH_LOGOUT } from "@/store/actions/auth.js";
export default {
  name: "AppDeveloper",
  methods: {
    // logout: function() {
    //   this.$store.dispatch(AUTH_LOGOUT).then(() => this.$router.push("/login"));
    // },
     downloadJSON: function(){
      var blob = new Blob([ JSON.stringify(this.form_values) ], { "type" : "text/plain" });
      let link = document.createElement('a')
      link.href = window.URL.createObjectURL(blob)
      link.download = 'model.json'
      link.click()
    },
    clicked:function(v){
        this.$modal.show(v);
    }
  },

  data() {
      let modls = [
          {
          model_name:"Model 1",
          endpoint:"www.modelendpoint.com",
          request_type:"{a:int}",
          response_type:"{b:int}",
          value:false
          },
          {
          model_name:"Model 2",
          endpoint:"www.modelendpoint.com",
                    request_type:"{a:int}",
          response_type:"{b:int}",
          value:false

          },
          {
          model_name:"Model 3",
          endpoint:"www.modelendpoint.com",
                    request_type:"{a:int}",
          response_type:"{b:int}",
          value:false

          },
      ];
       let sens = [
          {
          sensor_name:"sensor 1",
          endpoint:"www.sensorendpoint.com",
          request_type:"{a:int}",
          response_type:"{b:int}",
          value:false
          },
          {
          sensor_name:"sensor 2",
          endpoint:"www.sensorendpoint.com",
                    request_type:"{a:int}",
          response_type:"{b:int}",
          value:false

          },
          {
          sensor_name:"sensor 3",
          endpoint:"www.sensorendpoint.com",
                    request_type:"{a:int}",
          response_type:"{b:int}",
          value:false

          },
      ];
           let conts = [
          {
          controller_name:"controller 1",
          endpoint:"www.controllerendpoint.com",
          request_type:"{a:int}",
          response_type:"{b:int}",
          value:false
          },
          {
          controller_name:"controller 2",
          endpoint:"www.controllerendpoint.com",
                    request_type:"{a:int}",
          response_type:"{b:int}",
          value:false

          },
          {
          controller_name:"controller 3",
          endpoint:"www.controllerendpoint.com",
                    request_type:"{a:int}",
          response_type:"{b:int}",
          value:false

          },
      ];
  
    return {

      form_values : {},
      file:null,
      value:false,
      models:modls,
      sensors: sens,
      controllers:conts,
 


      

    }
  },
 
};
</script>
<style lang="scss" scoped>

// .span-float{
//   float:right;
// }
</style>
