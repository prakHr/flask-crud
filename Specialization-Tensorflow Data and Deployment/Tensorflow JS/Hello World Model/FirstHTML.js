var val,saveButton, clearButton;
var model;
function getModel(){
        const model = tf.sequential();
        model.add(tf.layers.dense({units: 1, inputShape: [1]}));
        model.compile({loss:'meanSquaredError', 
                       optimizer:'sgd'});
        //model.summary();
        return model;
}

async function train(model,xs,ys)
{

    return model.fit(xs, ys, 
            { epochs: 500,
                callbacks:{
                    onEpochEnd: async(epoch, logs) =>{
                        console.log("Epoch:" 
                            + epoch 
                            + " Loss:" 
                            + logs.loss);
                                  
                    }
                }
            });
}
function save() {
  val = document.getElementById('xs').value;
  val = parseInt(val);  
  var data =tf.tensor2d([val],[1,1]);
   //console.log("Here "+data);
   //Here Tensor
  // [[3],]
  var results = model.predict(data);
  //console.log("Here "+data);
  ///results.print();
  ///console.log(results.dataSync());
  ///alert(results.dataSync());
 	//var prediction=model.predict(tf.tensor2d([10],[1,1]));
 	//var pIndex=tf.argMax(prediction,1).dataSync();
 	//alert(pIndex);
 	document.getElementById('xs').value=results.dataSync();
}

function erase() {
  document.getElementById('xs').value="";
}

function init(){
  
  saveButton = document.getElementById('sb');
  saveButton.addEventListener("click", save);
  clearButton = document.getElementById('cb');
  clearButton.addEventListener("click", erase);
}

async function run(){
	const xs = tf.tensor2d([-1.0, 0.0, 1.0, 2.0, 3.0, 4.0], [6, 1]);
  	const ys = tf.tensor2d([-3.0, -1.0, 2.0, 3.0, 5.0, 7.0], [6, 1]);
        
    model = getModel();
    //tfvis.show.modelSummary({name: 'Model Architecture'}, model);
    await train(model,xs,ys);
    //console.log(model.summary()) ;
    init();
    alert("Training is done, try predicting your values!");
}

document.addEventListener('DOMContentLoaded', run);
