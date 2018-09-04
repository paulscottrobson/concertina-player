/// <reference path="../lib/phaser.comments.d.ts"/>

/**
 * Main Game class.
 * 
 * @class MainState
 * @extends {Phaser.State}
 */
class MainState extends Phaser.State {

    public static VERSION:string="0.93 11-Jun-18 Phaser-CE 2.8.7 (c) PSR 2017,8";

    init() {
        // Initialise config
        Configuration.initialise(this.game);
        // Load in music
        var json:any = this.game.cache.getJSON("music");
        // this.music = new Music(json);
    }

    create() {    
    }
    
    destroy() : void {
    }

    update() : void {
        // Time in milliseconds
        // var elapsedMS:number = this.game.time.elapsedMS;
        // Beats per millisecond
        // var bpms:number = this.music.getTempo() / 60 / 1000;
        // Bars per millisecond
        // bpms = bpms / this.music.getBeats() * this.speedControl.getScalar();
        //bpms = 0;
        // Work out new position.
        //this.pos = Math.min(this.music.getBarCount(),this.pos + bpms * elapsedMS);
        //this.pos = this.positionControl.updatePosition(this.pos);
        //this.pos = Math.min(this.music.getBarCount(),this.pos);
        //this.pos = Math.max(0,this.pos);
        //this.speedControl.updateRotate(elapsedMS);
        //this.manager.moveTo(this.pos);
        // Work out new bar / quarterbeat
        var bar:number = Math.floor(this.pos);
        var qBeat:number = Math.floor((this.pos-bar) * 4 * this.music.getBeats());
    }
}    
