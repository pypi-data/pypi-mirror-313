Usage Sample
''''''''''''

.. code:: python

        import pltx 

        y_true = [1, 1, 1, 0, 0, 0]
        y_pred = [1, 0, 1, 0, 0, 0]
        y_prob = [0.9, 0.1, 0.8, 0.2, 0.7, 0.3]

        pltx.plot_roc(y_true, y_prob)
        pltx.plot_confusion_matrix2(y_true, y_pred)
       
