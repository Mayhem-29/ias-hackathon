<template>
  <div
    uk-height-viewport="offset-bottom: 80px"
    class="uk-flex uk-flex-center uk-flex-middle uk-flex-column"
  >
    <h1>App Developer Form</h1>
    <FormulateForm
    class="login-form"
    v-model="form_values"
    @submit="downloadJSON"
  >
    <h2 class="form-title">Form</h2>
    <p>
     Please Fill the required information.
    </p>
    <span >
    <FormulateInput
      name="model_name"
      type="text"
      label="Model Name"
      placeholder="Model Name"
      validation="required"
    />
    <FormulateInput
      name="model_author"
      type="text"
      label="Model Author"
      placeholder="Model Author"
      validation="required"
    />
    </span>
    <span class="span-float">
    <FormulateInput
    type = "group"
    name = "model_input"
    :repeatable="true"
    label = "Model Input"
    add-label="Add Input"
    validation="required"
    #default="{ index }"
    >
       <FormulateInput
    name="input_number"
    type = "number"
    :value="index+1"
    />
        <FormulateInput
      name="input_type"
      :options="{string: 'String', float: 'Float', int : 'Int', image: 'Image'}"
      type="select"
      label="Input Type"
    />
 
    </FormulateInput>
    </span>
      <FormulateInput
      name="model_input_format"
      type="text"
      label="Model Input Format"
      placeholder="Model Input Format"
      validation="required"
    />
    <FormulateInput
      name="model_output"
      :options="{string: 'String', float: 'Float', int : 'Int', image: 'Image'}"
      type="select"
      label="Model Output"
    />
  
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
</style>
