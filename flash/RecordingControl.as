﻿package {	import flash.system.Capabilities;	import flash.net.URLVariables;	import uploadtools.UploadPostHelper;	import org.bytearray.micrecorder.MicRecorder;	import org.bytearray.micrecorder.encoder.WaveEncoder;	import org.bytearray.micrecorder.events.RecordingEvent;	import flash.events.Event;	import flash.events.SampleDataEvent;	import flash.net.URLRequest;	import flash.net.URLRequestHeader;	import flash.net.URLRequestMethod;	import flash.net.URLLoader;	import flash.net.URLLoaderDataFormat;	import flash.media.Sound;	import flash.net.FileReference;	import fr.kikko.lab.ShineMP3Encoder;			public class RecordingControl {		private var wavEncoder:WaveEncoder;		private var recorder:MicRecorder;				public function RecordingControl() {			wavEncoder = new WaveEncoder(.5);			recorder = new MicRecorder( wavEncoder );					recorder.addEventListener(RecordingEvent.RECORDING, onRecording);			recorder.addEventListener(Event.COMPLETE, onRecordComplete);		}		private function onRecording(event:RecordingEvent):void		{			//trace('recording');		}				private function onRecordComplete(event:Event):void		{			trace('recording completed');		}				public function start() {			recorder.record();		}		public function stop() {			recorder.stop();		}				public function sendFile():void		{        			var url:String = "http://127.0.0.1:8000/uploadtarget";			var urlRequest:URLRequest = new URLRequest();			urlRequest.url = url;			urlRequest.contentType = 'multipart/form-data; boundary=' + UploadPostHelper.getBoundary();			urlRequest.method = URLRequestMethod.POST;			urlRequest.data = UploadPostHelper.getPostData("fileupload.wav", recorder.output,"fileupload");			urlRequest.requestHeaders.push( new URLRequestHeader( 'Cache-Control', 'no-cache' ) );						var urlLoader:URLLoader = new URLLoader();			urlLoader.dataFormat = URLLoaderDataFormat.BINARY;			//urlLoader.addEventListener(Event.COMPLETE, onComplete);			//urlLoader.addEventListener(IOErrorEvent.IO_ERROR, onError);			//urlLoader.addEventListener(SecurityErrorEvent.SECURITY_ERROR, onError);			urlLoader.load(urlRequest);		}		public function sendMp3():void		{		                var mp3Encoder:ShineMP3Encoder;            mp3Encoder = new ShineMP3Encoder(recorder.output);            mp3Encoder.addEventListener(Event.COMPLETE, onFinishEncoding);            //mp3Encoder.addEventListener(ProgressEvent.PROGRESS, mp3EncodeProgress);            //mp3Encoder.addEventListener(ErrorEvent.ERROR, mp3EncodeError);            mp3Encoder.start();                        function onFinishEncoding(event:Event) {                trace('encoding complete');			    var url:String = "http://127.0.0.1:8000/uploadtarget";			    var urlRequest:URLRequest = new URLRequest();			    urlRequest.url = url;			    urlRequest.contentType = 'multipart/form-data; boundary=' + UploadPostHelper.getBoundary();			    urlRequest.method = URLRequestMethod.POST;			    urlRequest.data = UploadPostHelper.getPostData("fileupload.mp3", mp3Encoder.mp3Data,"fileupload");			    urlRequest.requestHeaders.push( new URLRequestHeader( 'Cache-Control', 'no-cache' ) );						    var urlLoader:URLLoader = new URLLoader();			    urlLoader.dataFormat = URLLoaderDataFormat.BINARY;			    //urlLoader.addEventListener(Event.COMPLETE, onComplete);			    //urlLoader.addEventListener(IOErrorEvent.IO_ERROR, onError);			    //urlLoader.addEventListener(SecurityErrorEvent.SECURITY_ERROR, onError);			    urlLoader.load(urlRequest);		    }	    }				public function playBack() {		    recorder.buffer.position = 0;			var sound:Sound = new Sound();			sound.addEventListener(SampleDataEvent.SAMPLE_DATA, playbackSampleHandler);			sound.play();		}				public function playbackSampleHandler(event:SampleDataEvent):void		{			for (var i:int = 0; i < 8192 && recorder.buffer.bytesAvailable > 0; i++) 			{				var sample:Number = recorder.buffer.readFloat();				event.data.writeFloat(sample);				event.data.writeFloat(sample);			}		}				public function exportMp3(completeCallback:Function):void {            var mp3Encoder:ShineMP3Encoder;            mp3Encoder = new ShineMP3Encoder(recorder.output);            mp3Encoder.addEventListener(Event.COMPLETE, onEncodingComplete);            //mp3Encoder.addEventListener(ProgressEvent.PROGRESS, mp3EncodeProgress);            //mp3Encoder.addEventListener(ErrorEvent.ERROR, mp3EncodeError);            mp3Encoder.start();                        function onEncodingComplete(event:Event) {                completeCallback(mp3Encoder.mp3Data);            }        }	}}