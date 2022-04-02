<template>
  <div
    uk-height-viewport="offset-bottom: 80px"
    class="uk-flex uk-flex-middle uk-flex-column"
  >
    <h1>Platform Admin</h1>
    <FormulateForm
    class="login-form"
    v-model="form_values"
    @submit="downloadJSON"
  >

   
    <span class="span-float">
    <FormulateInput
    type = "group"
    name = "sensor_data"
    :repeatable="true"
    label = "Sensor Data"
    add-label="Add Input"
    validation="required"
        >
     <FormulateInput
      name="sensor_type"
      type="select"
      :options="{type_a:'Type A',type_b:'Type B'}"
      label="Sensor Type"
      placeholder="Sensor Type"
      validation="required"
    />
        <FormulateInput
      name="sensor_ip"
      type="text"
      label="Sensor IP"
      placeholder="Sensor IP"
      validation="required"
    />
      <FormulateInput
      name="sensor_port"
      type="text"
      label="Sensor Port"
      placeholder="Sensor Port"
      validation="required"
    />
      <FormulateInput
      name="sensor_location"
      type="text"
      label="Sensor Location"
      placeholder="Sensor Location"
      validation="required"
    />
      <FormulateInput
      name="sensor_instance_count"
      type="number"
      label="Sensor Instance Count"
      placeholder="Sensor Instance Count"
      validation="required"
    />

     
 
    </FormulateInput>
    </span>
     
   
  
    <pre
      class="code"
      v-text="form_values"
    />
      <FormulateInput
      type="submit"
      label="Download"
    />
  </FormulateForm>
  </div>
</template>

<script>
import { AUTH_LOGOUT } from "@/store/actions/auth.js";
export default {
  name: "PlatformAdmin",
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
  },
  data() {
    return {
      form_values : {}

    }
  },
 
};
</script>
<style lang="scss" scoped>

// .span-float{
//   float:right;
// }
.login-form{
    width:800px;
}
</style>
