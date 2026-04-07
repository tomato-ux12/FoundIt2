import { Button } from "@/components/ui/button";
import { ArrowRight, Zap } from "lucide-react";

const Hero = () => {
  return (
    <section className="relative min-h-[90vh] flex items-center justify-center overflow-hidden">
      {/* Background glow */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-primary/5 rounded-full blur-3xl pointer-events-none" />

      <div className="container relative z-10 px-6 text-center max-w-4xl mx-auto">
        {/* Badge */}
        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full border border-border bg-surface text-sm text-muted-foreground mb-8 animate-fade-up">
          <Zap className="w-4 h-4 text-primary" />
          <span>Pour freelances SEO uniquement</span>
        </div>

        {/* Headline */}
        <h1 className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-black tracking-tight leading-[1.1] mb-6 animate-fade-up" style={{ animationDelay: "0.1s" }}>
          Arrête de coder des produits
          <br />
          que <span className="text-gradient">personne ne paie.</span>
        </h1>

        {/* Subheadline */}
        <p className="text-lg sm:text-xl text-muted-foreground max-w-2xl mx-auto mb-10 animate-fade-up" style={{ animationDelay: "0.2s" }}>
          FoundIt détecte les opportunités SaaS validées par la preuve d'argent.
          En 30 min, tu sais si ton idée vaut le coup — ou pas.
        </p>

        {/* CTA */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center items-center animate-fade-up" style={{ animationDelay: "0.3s" }}>
          <Button variant="hero" size="lg" className="text-base px-8 py-6 animate-pulse-glow">
            Rejoindre la waitlist
            <ArrowRight className="w-5 h-5 ml-1" />
          </Button>
        </div>

        {/* Proof line */}
        <p className="text-sm text-muted-foreground mt-6 animate-fade-up" style={{ animationDelay: "0.4s" }}>
          Essai 7 jours à 1€ · Pas de freemium · Pas de bullshit
        </p>

        {/* Preview mockup */}
        <div className="mt-16 animate-fade-up" style={{ animationDelay: "0.5s" }}>
          <div className="surface-card p-6 max-w-2xl mx-auto glow-border">
            <div className="text-left space-y-3">
              <p className="text-xs text-muted-foreground uppercase tracking-wider font-medium">10 opportunités validées pour toi</p>
              <div className="space-y-2">
                {[
                  { score: 87, color: "bg-score-green", label: "Audit technique hebdo automatisé", proofs: 47, price: "129€/mois" },
                  { score: 82, color: "bg-score-green", label: "Monitoring multi-clients GSC", proofs: 38, price: "89€/mois" },
                  { score: 71, color: "bg-score-yellow", label: "Rapports SEO white-label rapides", proofs: 29, price: "59€/mois" },
                ].map((item) => (
                  <div key={item.label} className="flex items-center gap-4 p-3 rounded-lg bg-background/50 border border-border/50 hover:border-primary/20 transition-colors cursor-pointer">
                    <div className={`flex-shrink-0 w-10 h-10 rounded-lg ${item.color} flex items-center justify-center text-sm font-bold text-primary-foreground`}>
                      {item.score}
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="font-medium text-sm truncate">{item.label}</p>
                      <p className="text-xs text-muted-foreground">{item.proofs} preuves · {item.price} moyen</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;
