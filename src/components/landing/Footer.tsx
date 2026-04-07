const Footer = () => {
  return (
    <footer className="border-t border-border py-12">
      <div className="container px-6 max-w-5xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="flex items-center gap-2">
          <span className="text-lg font-bold text-gradient">FoundIt</span>
        </div>
        <p className="text-sm text-muted-foreground">
          © {new Date().getFullYear()} FoundIt · validation ≠ revenu garanti
        </p>
      </div>
    </footer>
  );
};

export default Footer;
