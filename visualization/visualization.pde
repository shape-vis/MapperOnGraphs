
import usf.dvl.mog.*;

  FrameManager frameMgr;


   public void setup() {
    size(1600, 900, P3D);
    smooth(4);
    frameMgr = new FrameManager( this );
    frameMgr.setup();
  }


  public void fileSelected(File selection) {
    frameMgr.fileSelected(selection);
  }
  
   public void draw() { frameMgr.draw(); }
  
   public void keyPressed( ) { frameMgr.keyPressed(); } 
   public void mousePressed( ) { frameMgr.mousePressed(); }
   public void mouseReleased( ) { frameMgr.mouseReleased(); }
   public void mouseDragged( ) { frameMgr.mouseDragged(); }
   public void mouseWheel( MouseEvent e ) { frameMgr.mouseWheel(e); }
  
