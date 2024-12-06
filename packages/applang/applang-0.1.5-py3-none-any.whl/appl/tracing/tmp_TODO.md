## Events

* Function call and return events
  * record function code
  * record prompt records within the function
    * Question: how to build a one-to-one mapping between the code and the actual prompt?
* Completion call and response events
  * record prompt and parameters

## Serialization

* Serialize llm response into dict (should support loading)
* Serialize function inputs and outputs as dict of strings (do not need to support loading)

## Display

* Use React
  * serve a webpage in the folder
* index page:
  * Left:
    * display the traces in the folder, include some meta-data, like timestamp, name, etc.
  * Right:
    * display the custom log, with a button to display the minimized trace (clickable to trace page)
* trace page:
  * left: display the trace tree (allow collapse and expand)
    * function call and completion events
  * right: display the trace details
    * details of the selected event
    * function
      * code
      * input and output
      * prompt records
    * completion
      * prompt
      * response
  * should support edit and save (save as)
* Or make it a column view (every time one or two columns displayed)
  * order: trace files, custom log, trace tree, event details
