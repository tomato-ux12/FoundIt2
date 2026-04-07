import { Button } from "@/components/ui/button";

const Navbar = () => {
  return (
    <nav className="fixed top-0 left-0 right-0 z-50 border-b border-border/50 bg-background/80 backdrop-blur-xl">
      <div className="container px-6 max-w-5xl mx-auto flex items-center justify-between h-16">
        <span className="text-xl font-bold text-gradient">FoundIt</span>
        <Button variant="hero" size="sm">
          Rejoindre la waitlist
        </Button>
      </div>
    </nav>
  );
};

export default Navbar;
