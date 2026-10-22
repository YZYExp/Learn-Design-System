export interface ExhibitTitleProps {chinese?:string;english?:string;compact?:boolean}
export interface InfoStripProps {date?:string;hours?:string;venue?:string;address?:string}
export interface PictureFrameProps {src?:string;ratio?:string;position?:string}
export declare function ExhibitTitle(p?:ExhibitTitleProps): HTMLElement;
export declare function InfoStrip(p?:InfoStripProps): HTMLElement;
export declare function PictureFrame(p?:PictureFrameProps): HTMLElement;
