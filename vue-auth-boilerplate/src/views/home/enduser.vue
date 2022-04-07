<template>
  <div
    uk-height-viewport="offset-bottom: 80px"
    class=""
  >
    <h1>End User Form</h1>
    <ul uk-accordion>
    <li v-for="(item,index) in app_data" :key="item.app_name" >
        
        <FormulateInput
          v-model="app_data[index]['selected']"
          type="checkbox"
          class="check"
        />
        <a class="uk-accordion-title" href="#"> 
        {{item.app_name}}</a>
        <div class="uk-accordion-content">
            <FormulateForm
    class="login-form"
    v-model="app_data[index]"
  >
  <FormulateInput
  type="datetime-local"
  name="start_time"
  label="Start Time"
  placeholder="Start Time"
  help="Sample datetime-local help text"
  validation="required"
/>
<FormulateInput
  name="standalone"
  type="checkbox"
  label="Standalone"
/>
<FormulateInput
      name="duration"
      type="number"
      label="Duration"
      placeholder="Duration"
      validation="required"
    />

  </FormulateForm>
            <p v-for="sensor in item.sensors" :key="sensor.sensor_name" >{{sensor.sensor_type}} {{sensor.sensor_location}}</p>
        </div>
    </li>
    
</ul>
    <pre
      class="code"
      v-text="app_data"
    />
    
  </div>
</template>

<script>
import { AUTH_LOGOUT } from "@/store/actions/auth.js";
export default {
  name: "EndUser",
  methods: {
    
  },
  data() {
    let apps = [
      {
        start_time:null,
        duration:60,
        standalone:false,
        selected:false,
        app_name:"App 1",
        models:[
          {
            "model_name":"Model 1",
          },
          {
            "model_name":"Model 1",
          },

        ],
        sensors:[
          
             {
      "sensor_type": "type_a",
      "sensor_location": "12345:2344511",
          }

          ,
          {
  "sensor_type": "type_b",
      "sensor_location": "1234545:2344511",
          }
        ]
      },

       {
        start_time:null,
        duration:60,
        standalone:false,
        selected:false,
        app_name:"App 2",
        models:[
          {
            "model_name":"Model 3",
          },
          {
            "model_name":"Model 4",
          },

        ],
        sensors:[
          
             {
      "sensor_type": "type_c",
      "sensor_location": "12wertewsfg345:2344511",
          }

          ,
          {
  "sensor_type": "type_b",
      "sensor_location": "1234545:2344sdfgdr511",
          }
        ]
      }


    ];
    return {
      app_data:apps,
      form_values : {
      }

    }
  },
 
};
</script>
<style lang="scss" scoped>

// .span-float{
//   float:right;
// }
// .check{
//   float:right;
//   margin-right:20px;
//   margin-top:5px;
// }
</style>
