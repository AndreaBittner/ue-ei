package com.adafruit.bleuart;

import android.app.Activity;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothGattCharacteristic;
import android.net.Uri;
import android.os.Bundle;
import android.os.Environment;
import android.text.format.DateFormat;
import android.text.method.ScrollingMovementMethod;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import com.google.android.gms.appindexing.Action;
import com.google.android.gms.appindexing.AppIndex;
import com.google.android.gms.common.api.GoogleApiClient;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Date;
import android.util.Log;

public class MainActivity extends Activity implements BluetoothLeUart.Callback {

    // UI elements
    private TextView messages;
    private Button save;
    private Button stop;
    private Button start;
    private Button reset;
    private boolean shouldReconnect = false;

    private static class  microCommand {
        public static int START    = 1;
        public static int STOP     = 2;
        public static int RESET    = 3;
    }


    // Bluetooth LE UART instance.  This is defined in BluetoothLeUart.java.
    private BluetoothLeUart uart;
    /**
     * ATTENTION: This was auto-generated to implement the App Indexing API.
     * See https://g.co/AppIndexing/AndroidStudio for more information.
     */
    private GoogleApiClient client;

    private StringBuilder output;
    private StringBuilder output_saver;
    private int oldReceiveCounter;
    private int receiveCounter;
    // TODO Check
    // is true, after clickStart(), after connection lost, clickStart() shall be started automatically
    private Boolean receivingDataMode = false;

    private StringBuilder output(){
        if (output == null)
            output = new StringBuilder();
        return output;
    }

    private StringBuilder output_saver(){
        if (output_saver == null)
            output_saver = new StringBuilder();
        return output_saver;
    }

    // Write some text to the messages text view.
    // Care is taken to do this on the main UI thread so writeLine can be called from any thread
    // (like the BTLE callback).
    private void writeLine(final CharSequence text) {
        runOnUiThread(new Runnable() {
            @Override
            public void run() {
                messages.append(text);
                //messages.append("\n");
            }
        });
    }
    private void writeLine(final Integer counter) {
        runOnUiThread(new Runnable() {
            @Override
            public void run() {
                messages.append(counter.toString());
                messages.append("\n");
            }
        });
    }

    private void sendCommand(int command) {
        uart.send(command+"");
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // Grab references to UI elements.
        messages = (TextView) findViewById(R.id.messages);
        // Initialize UART.
        uart = new BluetoothLeUart(getApplicationContext());

        // Disable the save button until we're connected.
        save = (Button) findViewById(R.id.save);
        save.setClickable(false);
        save.setEnabled(false);
        start = (Button) findViewById(R.id.start);
        start.setClickable(false);
        start.setEnabled(false);
        stop = (Button) findViewById(R.id.stop);
        stop.setClickable(false);
        stop.setEnabled(false);
        reset = (Button) findViewById(R.id.reset);
        reset.setClickable(true);
        reset.setEnabled(true);

        // Enable auto-scroll in the TextView
        messages.setMovementMethod(new ScrollingMovementMethod());
        // ATTENTION: This was auto-generated to implement the App Indexing API.
        // See https://g.co/AppIndexing/AndroidStudio for more information.
        client = new GoogleApiClient.Builder(this).addApi(AppIndex.API).build();
    }

    // OnCreate, called once to initialize the activity.
    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.main, menu);
        return true;
    }

    // OnResume, called right before UI is displayed.  Connect to the bluetooth device.
    @Override
    protected void onResume() {
        super.onResume();
        writeLine("Scanning for devices ...\n");

        uart.registerCallback(this);
        uart.connectFirstAvailable();
    }

    // OnStop, called right before the activity loses foreground focus.  Close the BTLE connection.
    @Override
    protected void onStop() {
        super.onStop();
        // ATTENTION: This was auto-generated to implement the App Indexing API.
        // See https://g.co/AppIndexing/AndroidStudio for more information.
        Action viewAction = Action.newAction(
                Action.TYPE_VIEW, // TODO: choose an action type.
                "Main Page", // TODO: Define a title for the content shown.
                // TODO: If you have web page content that matches this app activity's content,
                // make sure this auto-generated web page URL is correct.
                // Otherwise, set the URL to null.
                Uri.parse("http://host/path"),
                // TODO: Make sure this auto-generated app URL is correct.
                Uri.parse("android-app://com.adafruit.bleuart/http/host/path")
        );
        AppIndex.AppIndexApi.end(client, viewAction);
        uart.unregisterCallback(this);
        uart.disconnect();
        // ATTENTION: This was auto-generated to implement the App Indexing API.
        // See https://g.co/AppIndexing/AndroidStudio for more information.
        client.disconnect();
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();
        if (id == R.id.action_settings) {
            return true;
        }
        return super.onOptionsItemSelected(item);
    }

    // UART Callback event handlers.
    @Override
    public void onConnected(BluetoothLeUart uart) {
        // Called when UART device is connected and ready to receive data.
        writeLine("Connected!\n");
        // Enable the save button
        runOnUiThread(new Runnable() {
            @Override
            public void run() {
                save = (Button) findViewById(R.id.save);
                save.setClickable(true);
                save.setEnabled(true);
                start = (Button) findViewById(R.id.start);
                start.setClickable(true);
                start.setEnabled(true);
                stop = (Button) findViewById(R.id.stop);
                stop.setClickable(true);
                stop.setEnabled(true);
            }
        });
        if (receivingDataMode) {
            clickStart(start);
        }

        shouldReconnect = false;
    }

    @Override
    public void onConnectFailed(BluetoothLeUart uart) {
        // Called when some error occured which prevented UART connection from completing.
        writeLine("Error connecting to device!\n");
        DeactivateButtons();
    }

    private void DeactivateButtons() {
        runOnUiThread(new Runnable() {
            @Override
            public void run() {
                save = (Button) findViewById(R.id.save);
                save.setClickable(false);
                save.setEnabled(false);
                start = (Button) findViewById(R.id.start);
                start.setClickable(false);
                start.setEnabled(false);
                stop = (Button) findViewById(R.id.stop);
                stop.setClickable(false);
                stop.setEnabled(false);
            }
        });
    }

    @Override
    public void onDisconnected(BluetoothLeUart uart2) {
        // Called when the UART device disconnected.
        writeLine("Disconnected!\n");
        // Disable the save button.
        runOnUiThread(new Runnable() {
            @Override
            public void run() {
                save = (Button) findViewById(R.id.save);
                save.setClickable(true);
                save.setEnabled(true);
                start = (Button) findViewById(R.id.start);
                start.setClickable(false);
                start.setEnabled(false);
                stop = (Button) findViewById(R.id.stop);
                stop.setClickable(false);
                stop.setEnabled(false);
            }
        });
    }

    @Override
    public void onReceive(BluetoothLeUart uart, BluetoothGattCharacteristic rx) {
        // Called when data is received by the UART.
        if(receiveCounter % 100 == 0) {
            writeLine(receiveCounter);
        }
        receiveCounter++;
        output().append(rx.getStringValue(0));
        Log.d("RECEIVE", rx.getStringValue(0) + " #UART " + uart.toString());
    }

    @Override
    public void onDeviceFound(BluetoothDevice device) {
        // Called when a UART device is discovered (after calling startScan).
        writeLine("Found device : " + device.getAddress() + "\n");
        writeLine("Waiting for a connection ...\n");
    }

    @Override
    public void onDeviceInfoAvailable() {
        writeLine(uart.getDeviceInfo());
    }

    @Override
    public void onStart() {
        super.onStart();

        // ATTENTION: This was auto-generated to implement the App Indexing API.
        // See https://g.co/AppIndexing/AndroidStudio for more information.
        client.connect();
        Action viewAction = Action.newAction(
                Action.TYPE_VIEW, // TODO: choose an action type.
                "Main Page", // TODO: Define a title for the content shown.
                // TODO: If you have web page content that matches this app activity's content,
                // make sure this auto-generated web page URL is correct.
                // Otherwise, set the URL to null.
                Uri.parse("http://host/path"),
                // TODO: Make sure this auto-generated app URL is correct.
                Uri.parse("android-app://com.adafruit.bleuart/http/host/path")
        );
        AppIndex.AppIndexApi.start(client, viewAction);
    }

    // Handler for mouse click on the save button.
    public void clickSave(View view) {
         saveFile();
    }

    private void saveFile() {
        StringBuilder temp;
        temp = output_saver();
        output_saver = output();
        output = temp;

        File sdCard = Environment.getExternalStorageDirectory();
        File dir = new File(sdCard.getAbsolutePath() + "/Download");

        Date d = new Date();
        CharSequence s  = DateFormat.format("MMddyy_hhmmss", d.getTime());
        File file = new File(dir, s.toString() + "_data_" + oldReceiveCounter + "-" + receiveCounter + ".txt");
        FileWriter filewriter;

        try {
            filewriter = new FileWriter(file);
            filewriter.write(output_saver().toString());
            filewriter.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
        output_saver.setLength(0);
        oldReceiveCounter = receiveCounter;
        writeLine("\n-- SAVED --\n");
    }

    public void clickStart(View view){
        receivingDataMode = true;
        output().setLength(0);
        sendCommand(microCommand.START);
        writeLine("\n-- START --\n");
    }

    public void clickStop(View view) {
        //Werte in App lassen, Stringbuffer beibehalten, Speichern als File noch möglich
        //Stoppt nur Werte Senden des Mikrocontrollers
        sendCommand(microCommand.STOP);
        receivingDataMode = false;
        writeLine("\n-- STOP -- Click SAVE to save data now\n");
    }

    public void clickReset(View view) {
        clickSave(view);
        sendCommand(microCommand.RESET);
        receiveCounter = 0;
        oldReceiveCounter = 0;
        output().setLength(0);
        messages.setText("");
        uart.connectFirstAvailable();
        writeLine("-- Wait for Reset ... --\n");
    }
}
